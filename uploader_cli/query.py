#!/usr/bin/python
"""These are the query methods used for interactive query."""
from sys import stdin, stdout
from pager import page


def find_leaf_node(md_update):
    """Find a leaf node that has all deps resolved."""
    query_obj = md_update[0]
    for obj in md_update:
        if not bool(obj.value):
            dep_meta_ids = md_update.dependent_meta_id(obj.metaID)
            if dep_meta_ids:
                if set([bool(md_update[dep_id].value) for dep_id in dep_meta_ids]) == set([True]):
                    query_obj = obj
                    break
            else:
                query_obj = obj
                break
    md_update.update_parents(query_obj.metaID)
    return query_obj


def paged_content(title, display_data, valid_ids):
    """Display the data yielding results."""
    yield """
{} - Select an ID
=====================================
""".format(title)
    for _id in sorted(valid_ids):
        yield display_data[_id]


def interactive_select_loop(md_update, query_obj, default_id):
    """While loop to ask users what they want to select."""
    valid_ids = []
    display_data = {}
    for obj in md_update[query_obj.metaID].query_results:
        valid_ids.append(str(obj['_id']))
        display_data[str(obj['_id'])] = md_update[query_obj.metaID].displayFormat.format(**obj)
    selected_id = False
    while not selected_id:
        page(paged_content(query_obj.displayTitle, display_data, valid_ids))
        stdout.write('Select ID ({}): '.format(default_id))
        selected_id = stdin.readline().strip()
        if not selected_id:
            selected_id = default_id
        if str(selected_id) not in valid_ids:
            selected_id = False
    return selected_id


def set_results(md_update, query_obj, passed_id=False, interactive=False):
    """Set results of the query and ask if interactive."""
    if passed_id:
        default_id = passed_id
    else:
        default_id = md_update[query_obj.metaID].value
    if interactive:
        # dump the results to a pager
        selected_id = interactive_select_loop(md_update, query_obj, default_id)

    if selected_id != md_update[query_obj.metaID].value:
        new_obj = query_obj._replace(value=selected_id)
        md_update[query_obj.metaID] = new_obj


def query_main(md_update, args):
    """Query from the metadata configuration."""
    while not md_update.is_valid():
        query_obj = find_leaf_node(md_update)
        set_results(md_update, query_obj, getattr(args, query_obj.metaID, False), args.interactive)
    print [(obj.metaID, obj.value) for obj in md_update]
