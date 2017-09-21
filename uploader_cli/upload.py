#!/usr/bin/python
"""The upload module used to send the data to ingest."""
from threading import Thread
from json import dumps
from copy import deepcopy
from sys import stdout
from os import pipe, fdopen, walk, stat
from os.path import isfile, isdir, join
from time import sleep
from datetime import datetime
import logging
from uploader import Uploader, bundler


BLOCK_SIZE = 1024 * 1024
LOGGER = logging.getLogger(__name__)


def upload_files_from_args(file_list, followsymlinks):
    """Generate a files structure required by bundler."""
    ret = []
    for path in file_list:
        if isdir(path):
            for root, _dirs, files in walk(path, followsymlinks=followsymlinks):
                for fname in files:
                    name = join(root, fname)
                    ret.append({
                        'name': 'data/{}'.format(name),
                        'size': stat(name).st_size,
                        'mtime': stat(name).st_mtime,
                        'fileobj': open(name, 'rb')
                    })
        elif isfile(path):
            ret.append({
                'name': 'data/{}'.format(path),
                'size': stat(path).st_size,
                'mtime': stat(path).st_mtime,
                'fileobj': open(path, 'rb')
            })
    return ret


def check_okay(status):
    """Check if the status is something wrong."""
    return status['state'] == 'OK'


def check(status):
    """Check the status since it's complicated."""
    check = status['state'] != 'OK'
    check |= status['task'] != 'ingest metadata'
    check |= int(float(status['task_percent'])) != 100
    return check


def save_local(rfd, wfd, save_filename):
    """Save the bytes from rfd to args.savelocal and wfd."""
    with open(save_filename, 'w') as sfd:
        buf = rfd.read(BLOCK_SIZE)
        while buf:
            sfd.write(buf)
            wfd.write(buf)
            buf = rfd.read(BLOCK_SIZE)
    rfd.close()
    wfd.close()


def tar_in_tar(rfd, wfd, md_update, bundle_size):
    """Generate another bundler and wrap rfd in that tar."""
    upload_files = [{
        'fileobj': rfd,
        'name': 'data/data.tar',
        'size': bundle_size,
        'mtime': (datetime.now() - datetime(1970, 1, 1)).total_seconds()
    }]
    bundle = bundler.Bundler(md_update, upload_files)
    bundle.stream(wfd)
    rfd.close()
    wfd.close()


def setup_chain_thread(rfd, wfd, args, func, wthreads, doit):
    """Setup a local thread if we doit using func."""
    if doit:
        crfd, cwfd = pipe()
        crfd = fdopen(crfd, 'rb')
        cwfd = fdopen(cwfd, 'wb')
        my_args = [rfd, cwfd]
        my_args.extend(args)
        wthread = Thread(target=func, args=my_args)
        wthread.daemon = True
        wthread.start()
        wthreads.append(wthread)
        LOGGER.debug('Done with creating worker thread.')
        return crfd, wfd
    return rfd, wfd


def get_size_of_tar(md_update, args):
    """Get the size of the tar file, no tarintar."""
    stdout.write('Determining size of tar: ')
    rfd, wfd = pipe()
    rfd = fdopen(rfd, 'rb')
    wfd = fdopen(wfd, 'wb')
    length = 0
    wthreads = []
    setup_bundler(wfd, deepcopy(md_update), args, wthreads)
    buf = 'blarg'
    while buf:
        buf = rfd.read(BLOCK_SIZE)
        length += len(buf)
    LOGGER.debug('Waiting for bundler thread to complete.')
    for wthread in wthreads:
        wthread.join()
    stdout.write('Done {}.\n'.format(length))
    return length


def get_size_of_tar_in_tar(md_update, args, tar_size):
    """Return the content-length for the upload."""
    stdout.write('Determining size of tar in tar: ')
    rfd, wfd = pipe()
    rfd = fdopen(rfd, 'rb')
    wfd = fdopen(wfd, 'wb')
    length = 0
    wthreads = []
    rfd, wfd = setup_chain_thread(rfd, wfd, (deepcopy(md_update), tar_size), tar_in_tar, wthreads, True)
    setup_bundler(wfd, md_update, args, wthreads)
    buf = 'blarg'
    while buf:
        buf = rfd.read(BLOCK_SIZE)
        length += len(buf)
    for wthread in wthreads:
        wthread.join()
    stdout.write('Done {}.\n'.format(length))
    return length


def upload_main(md_update, args):
    """Main upload method."""
    if args.dry_run:
        return
    LOGGER.debug('Starting Upload.')
    tar_size = get_size_of_tar(deepcopy(md_update), args)
    tar_in_tar_size = 0
    content_length = tar_size
    LOGGER.debug('Size of tar %s tar_in_tar %s', md_update, deepcopy(md_update))
    if args.tarintar:
        tar_in_tar_size = get_size_of_tar_in_tar(deepcopy(md_update), args, tar_size)
        content_length = tar_in_tar_size
    LOGGER.debug('Size of tar %s tar_in_tar %s', tar_size, tar_in_tar_size)
    rfd, wfd = pipe()
    rfd = fdopen(rfd, 'rb')
    wfd = fdopen(wfd, 'wb')
    wthreads = []
    rfd, wfd = setup_chain_thread(rfd, wfd, (deepcopy(md_update), tar_size), tar_in_tar, wthreads, args.tarintar)
    rfd, wfd = setup_chain_thread(rfd, wfd, (args.localsave,), save_local, wthreads, args.localsave)
    setup_bundler(wfd, md_update, args, wthreads)
    up_obj = Uploader()
    LOGGER.debug('Starting with rfd (%s) and wfd (%s) and %s threads %s', rfd, wfd, len(wthreads), content_length)
    jobid = up_obj.upload(rfd, content_length=content_length)
    for wthread in wthreads:
        wthread.join()
    LOGGER.debug('Threads completd')
    rfd.close()
    if not args.wait:
        print('Not Waiting Job ID ({})'.format(jobid))
        return 0
    print('Waiting job to complete ({}).'.format(jobid))
    status = up_obj.getstate(jobid)
    while check_okay(status) and check(status):
        sleep(1)
        status = up_obj.getstate(jobid)
    print('Done.')
    print(dumps(status, sort_keys=True, indent=4, separators=(',', ': ')))
    return 0


def setup_bundler(wfd, md_update, args, wthreads):
    """Setup the bundler or local retry if passed."""
    if args.localretry:
        def read_bundle():
            """Read a bundle and send it to wfd."""
            with open(args.localretry, 'rb') as rfd:
                buf = rfd.read(BLOCK_SIZE)
                while buf:
                    wfd.write(buf)
                    buf = rfd.read(BLOCK_SIZE)
            wfd.close()
            LOGGER.debug('Done with reading bundle.')
        wthread = Thread(target=read_bundle)
        wthread.daemon = True
        wthread.start()
        wthreads.append(wthread)
        return

    def make_bundle():
        """Make the bundler out of files on cmdline."""
        upload_files = upload_files_from_args(args.files, args.followsymlinks)
        LOGGER.debug(upload_files)
        LOGGER.debug(md_update)
        bundle = bundler.Bundler(md_update, upload_files)
        bundle.stream(
            wfd,
            callback=lambda x: stdout.write('\r'+' '*80+'\r{:03.2f}%\r'.format(x*100)),
            sleeptime=2
        )
        wfd.close()
        stdout.write('\r        \r')
        LOGGER.debug('Done with making bundle.')
    wthread = Thread(target=make_bundle)
    wthread.daemon = True
    wthread.start()
    wthreads.append(wthread)
