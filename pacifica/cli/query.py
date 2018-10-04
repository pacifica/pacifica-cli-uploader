#!/usr/bin/python
# -*- coding: utf-8 -*-
"""These are the query methods used for interactive query."""
from __future__ import print_function
from sys import stdin, stdout, stderr
from subprocess import Popen, PIPE
from os import getenv, pathsep, path
import re
from six import text_type, PY2


def set_query_obj(dep_meta_ids, md_update, obj):
    """Return the query object or false."""
    if dep_meta_ids:
        if set([bool(md_update[dep_id].value) for dep_id in dep_meta_ids]) == set([True]):
            return obj
        return None
    return obj


def find_leaf_node(md_update):
    """Find a leaf node that has all deps resolved."""
    query_obj = md_update[0]
    for obj in md_update:
        if not bool(obj.value):
            dep_meta_ids = md_update.dependent_meta_id(obj.metaID)
            query_obj = set_query_obj(dep_meta_ids, md_update, obj)
            if query_obj:
                break
    md_update.update_parents(query_obj.metaID)
    return md_update[query_obj.metaID]


def paged_content(title, display_data, valid_ids):
    """Display the data yielding results."""
    num_re = re.compile('[0-9][0-9]')

    def id_cmp(a_id, b_id):
        """Compare two IDs by grabbing as many numbers as we can."""
        int_a = int(num_re.match(a_id).group(0))
        int_b = int(num_re.match(b_id).group(0))
        return int_a < int_b
    yield text_type("""
{} - Select an ID
=====================================
""").format(title)
    if PY2:  # pragma: no cover python 2 only
        sort_args = {'cmp': id_cmp}
    else:  # pragma: no cover python 3+ only
        from functools import cmp_to_key
        sort_args = {'key': cmp_to_key(id_cmp)}
    for _id in sorted(valid_ids, **sort_args):
        yield display_data[_id]


def format_query_results(md_update, query_obj):
    """Format the query results and return some data structures."""
    valid_ids = []
    display_data = {}
    for obj in md_update[query_obj.metaID].query_results:
        valid_ids.append(text_type(obj['_id']))
        display_data[text_type(
            obj['_id'])] = md_update[query_obj.metaID].displayFormat.format(**obj)
    return (valid_ids, display_data)


def set_selected_id(selected_id, default_id, valid_ids):
    """Return the selected ID validating it first."""
    if not selected_id:
        selected_id = default_id
    if text_type(selected_id) not in valid_ids:
        selected_id = False
    return selected_id


def parse_command(exe):
    """Walk the system path and return executable path."""
    real_cmd = None
    for ext in getenv('PATHEXT', '').split(pathsep):  # pragma: no branch
        for binpath in getenv('PATH').split(pathsep):  # pragma: no branch
            check_cmd = path.join(binpath, exe.strip()) + ext
            if path.isfile(check_cmd):  # pragma: no branch
                real_cmd = check_cmd
                break
        if real_cmd:  # pragma: no branch
            break
    return real_cmd


def execute_pager(content):
    """Find the appropriate pager default is embedded python pager."""
    pager_default = ['python', '-m', 'pager', '-']
    pager_exes = [
        getenv('PAGER', 'more').split(),
        ['more'],
        ['less'],
        ['most']
    ]
    for pager_exe in pager_exes:
        if not (pager_exe and pager_exe[0]):  # pragma: no cover simple check to see if pager is something
            continue
        pager_full_path = parse_command(pager_exe[0])
        if pager_full_path:
            pager_default = pager_exe
            pager_default[0] = pager_full_path
            break
    pager_proc = Popen(
        pager_default,
        stdin=PIPE,
        stdout=stdout,
        stderr=stderr
    )
    pager_proc.communicate(text_type('\n').join(content).encode('utf-8'))
    return pager_proc.wait()


def interactive_select_loop(md_update, query_obj, default_id):
    """While loop to ask users what they want to select."""
    valid_ids, display_data = format_query_results(md_update, query_obj)
    selected_id = False
    if len(valid_ids) == 1:
        return valid_ids[0]
    while not selected_id:
        execute_pager(paged_content(
            query_obj.displayTitle, display_data, valid_ids))
        stdout.write(text_type('Select ID ({}): ').format(default_id))
        selected_id = stdin.readline().strip()
        selected_id = set_selected_id(selected_id, default_id, valid_ids)
    return selected_id


def set_results(md_update, query_obj, default_id, interactive=False):
    """Set results of the query and ask if interactive."""
    if interactive:
        selected_id = interactive_select_loop(md_update, query_obj, default_id)
    else:
        print_text = text_type('Setting {} to {}.').format(
            query_obj.metaID, default_id)
        if PY2:  # pragma: no cover python 2 only
            print_text = print_text.encode('utf8')
        print(print_text)
        selected_id = default_id
    if selected_id != md_update[query_obj.metaID].value:
        new_obj = query_obj._replace(value=selected_id)
        md_update[query_obj.metaID] = new_obj


def filter_results(md_update, query_obj, regex):
    """Filter the results of query_obj by regex and save result back into md_update."""
    reg_engine = re.compile(regex, re.UNICODE)
    _valid_ids, display_data = format_query_results(md_update, query_obj)
    filtered_results = []
    for index in range(len(query_obj.query_results)):
        res = query_obj.query_results[index]
        if reg_engine.search(display_data[text_type(res['_id'])]):
            filtered_results.append(query_obj.query_results[index])
    md_update[query_obj.metaID] = query_obj._replace(
        query_results=filtered_results)
    valid_ids, display_data = format_query_results(md_update, query_obj)
    if valid_ids and query_obj.value not in valid_ids:
        md_update[query_obj.metaID] = query_obj._replace(
            value=filtered_results[0]['_id'])


def query_main(md_update, args):
    """Query from the metadata configuration."""
    while not md_update.is_valid():
        query_obj = find_leaf_node(md_update)
        regex = getattr(args, '{}_regex'.format(query_obj.metaID))
        if not regex:
            regex = text_type('.*')
        filter_results(md_update, query_obj, regex)
        default_id = getattr(args, query_obj.metaID, None)
        if not default_id:
            default_id = md_update[query_obj.metaID].value
        set_results(
            md_update,
            query_obj,
            default_id,
            args.interactive
        )
        if not md_update[query_obj.metaID].value:
            raise RuntimeError(
                text_type('Could not find value for {}').format(query_obj.metaID))
    return md_update
