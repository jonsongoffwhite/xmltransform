import xml.etree.ElementTree as ET
import logging
import sys

'''
Takes path array and finds node specified by path,
from root.
Applies function 'transform' to the calculated node
split_path is [(path, occurence), ...]
Returns the modified root
'''
def get_node_and_apply(root, split_path, transform, **kwargs):
    # Root is first location so can be skipped
    split_path = split_path[1:]
    curr = root
    for single_dir in split_path:
        dir_name = single_dir[0]
        index = single_dir[1]

        curr = root.findall(dir_name)[index]
    transform(curr, **kwargs)
    return root

'''
Same as above but for use with commands in which the final
directory of the path is not another tag, but an attribute
(preceded by '@'), or a text/comment block, e.g. 'text()'
'''
def get_parent_and_apply(root, split_path, transform, **kwargs):
    return get_node_and_apply(root, split_path[:-1], transform, **kwargs)

'''
Helper function to edit indexed contained elements like text()
'''
def set_text_at_index(par, contained_name, contained_index, new_text):
    texts = []
    for node in par.iter():
        if node == par:
            texts.append((node, node.text, False))
        else:
            texts.append((node, node.tail, True))
    relevant_segment = texts[contained_index]
    if relevant_segment[2]:
        relevant_segment[0].tail = new_text 
    else:
        relevant_segment[0].text = new_text


'''
For use with INSERT_AFTER and MOVE_AFTER
'''
def insert_node_after_text_at_index(par, contained_name, contained_index, node_to_insert):
    texts = []
    for node in par.iter():
        if node == par:
            texts.append((node, node.text, False))
        else:
            texts.append((node, node.tail, True))
    relevant_segment = texts[contained_index]

    #  If it's a tail value, we need node after
    #  If there isn't one after, we put it last
    if relevant_segment[2]:
        node_before = relevant_segment[0]
        node_i = list(curr).find(node_before)+1
        if len(list(curr)) > (node_i + 1):
            # Put it last
            par.append(element)
        else:
            par.insert(node_i, element)
    else:
        # Put it first
        par.insert(0, element)

''' RENAME '''

# Node transformation
def transform_rename_tag(curr, **kwargs):
    curr.tag = kwargs['new_name'] 

# Parent transformation
def transform_rename_attrib(curr, **kwargs):
    attrib = kwargs['attrib']
    new_name = kwargs['new_name']
    old_value = curr.attrib.pop(attrib) 
    curr.attrib[new_name] = old_value

''' UPDATE '''

# Parent transformation
def transform_update_attrib(curr, **kwargs):
    attrib = kwargs['attrib']
    value = kwargs['value']
    curr.attrib[attrib] = value

# Parent transformation
def transform_update_contained(curr, **kwargs):
    contained_name = kwargs['contained']
    index = kwargs['index']
    value = kwargs['value']
    texts = []
    set_text_at_index(curr, contained_name, index, value)
    # TODO: Only functions for text() currently, add support for comment()


''' APPEND_FIRST '''

# Node transformation
def transform_append_first(curr, **kwargs):
    value = kwargs['value']
    element = ET.fromstring(value)
    curr.insert(0, element)

''' APPEND '''

# Node transformation
def transform_append(curr, **kwargs):
    value = kwargs['value']
    element = ET.fromstring(value)
    curr.append(element)

''' INSERT_AFTER '''

# Parent transformation
def transform_insert_after_contained(curr, **kwargs):
    value = kwargs['value']
    contained_name = kwargs['contained_name']
    contained_index = kwargs['contained_index']
    node_to_insert = ET.fromstring(value)
    insert_node_after_text_at_index(curr, contained_name, contained_index, node_to_insert)

# Parent transformation
def transform_insert_after_tag(curr, **kwargs):
    tag_name = kwargs['tag_name']
    tag_index = kwargs['tag_index']
    value = kwargs['value']
    indices = [i for i, x in enumerate(curr) if x.tag == tag_name]
    new_index = indices[tag_index] + 1
    curr.insert(new_index, ET.fromstring(value))


''' MOVE_FIRST '''

# TODO: Implement for contained
# Parent transformation
def transform_move_first(curr, **kwargs):
    new_location = kwargs['new_location']
    tree_root = kwargs['tree_root']
    src_name = kwargs['src_name']
    src_index = kwargs['src_index']

    src_parent = curr
    src = curr.findall(src_name)[src_index]

    node = tree_root 
    for loc in new_location[1:]:
       node = node.findall(loc[0])[loc[1]]

    dst = node 

    src_parent.remove(src)
    dst.insert(0, src)


''' MOVE_AFTER '''

# TODO: Implement for contained
# Parent transformation
def transform_move_after(curr, **kwargs):
    new_location = kwargs['new_location']
    tree_root = kwargs['tree_root']
    src_name = kwargs['src_name']
    src_index = kwargs['src_index']

    src_parent = curr
    src = curr.findall(src_name)[src_index]

    node = tree_root 
    # Omit last location, as it is at same level
    for loc in new_location[1:-1]:
       node = node.findall(loc[0])[loc[1]]

    dst = node 
    dst_before_name = new_location[-1][0]
    dst_before_index = new_location[-1][1] 

    indices = [i for i, x in enumerate(dst) if x.tag == dst_before_name]
    new_index = indices[dst_before_index] 

    src_parent.remove(src)
    dst.insert(new_index, src)

''' REMOVE '''

# Parent transformation
def transform_remove_tag(curr, **kwargs):
    rem_name = kwargs['rem_name']
    rem_index = kwargs['rem_index']
    child = curr.findall(rem_name)[rem_index]
    curr.remove(child)

# Parent transformation
def transform_remove_contained(curr, **kwargs):
    contained_name = kwargs['contained_name']
    contained_index = kwargs['contained_index']
    set_text_at_index(curr, contained_name, contained_index, None)

