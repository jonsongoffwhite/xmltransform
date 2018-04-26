import xml.etree.ElementTree as ET
import logging
import sys

logging.basicConfig( stream=sys.stderr )
logging.getLogger( "tree_operations" ).setLevel( logging.DEBUG )
log= logging.getLogger( "tree_operations" )


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

        curr = curr.findall(dir_name)[index]
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

def get_text_at_index(par, contained_name, contained_index) -> str:
    texts = []
    for node in par.iter():
        if node == par:
            texts.append((node, node.text, False))
        else:
            texts.append((node, node.tail, True))
    relevant_segment = texts[contained_index]
    if relvant_segment[2]:
        return relevant_segment[0].tail
    else:
        return relevant_segment[0].text

def detach_apply_reattach(node, transformation):
    pass

'''
For use with INSERT_AFTER and MOVE_AFTER
'''
def insert_node_after_text_at_index(par, contained_name, contained_index, node_to_insert):
    texts = []
    for node in par.iter():
        if node == par:
            if node.text:
                texts.append((node, node.text, False))
        else:
            if node.tail:
                texts.append((node, node.tail, True))

    relevant_segment = texts[contained_index]

    #  If it's a tail value, we need node after
    #  If there isn't one after, we put it last
    if relevant_segment[2]:
        node_before = relevant_segment[0]
        node_i = list(par).index(node_before)+1
        if len(list(par)) > (node_i + 1):
            # Put it last
            par.append(node_to_insert)
        else:
            par.insert(node_i, node_to_insert)
    else:
        # Put it first
        par.insert(0, node_to_insert)

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

    # Find a better way of doing this
    # Detect if new attribute
    # Maybe outside call here? separate function?
    if len(value) > 1 and value.lstrip()[1] == '@':
        content = value.lstrip()
        content = '<' + content[2:]
        attr_tag = ET.fromstring(content)
        attr_value = attr_tag.text.strip()
        attr_name = attr_tag.tag
        curr.attrib[attr_name] = attr_value
    else:

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
    #if new_index >= len(list(curr)):
        # Insert last
    #    curr.append(ET.fromstring(value))
    #else:
    curr.insert(new_index, ET.fromstring(value))


''' MOVE_FIRST '''

# TODO: Implement for contained
# Parent transformation
def transform_move_first_tag(curr, **kwargs):
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

def transform_move_first_attribute(curr, **kwargs):
    new_location = kwargs['new_location']
    tree_root = kwargs['tree_root']
    src_name = kwargs['src_name']

    src_parent = curr
    attr_value = src_parent.attrib[src_name]
    # Remove attrib from parent
    del src_parent.attrib[src_name]

    node = tree_root
    for loc in new_location[1:]:
        node = node.findall(loc[0])[loc[1]]
    dst = node

    node.attrib[src_name] = attr_value

# Parent transformation
#def transform_move_first_contained(curr, **kwargs):
#    contained_name = kwargs['contained_name']
#    contained_index = kwargs['contained_index']

''' MOVE_AFTER '''

# TODO: Implement for contained
# Parent transformation
def transform_move_after_tag(curr, **kwargs):
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

    # Remove first as it could maintain the same parent
    src_parent.remove(src)
    indices = [i for i, x in enumerate(dst) if x.tag == dst_before_name]
    new_index = indices[dst_before_index]+1 

    dst.insert(new_index, src)

# Parent transformation
def transform_move_after_contained(curr, **kwargs):
    src_name = kwargs['src_name']
    src_index = kwargs['src_index']
    tree_root = kwargs['tree_root']
    destination = kwargs['destination']

    src_parent = curr
    src = src_parent.findall(src_name)[src_index]

    # Get the one before the src to reattach the tail,
    # If there isn't one (i.e. it is first), attach as text to parent
    # TODO: Clarify behaviour if there is already text there
    
    # No need to reattach as if moving a node after contained,
    # there is no chance it will have text after it
    before_actual_index = list(src_parent).index(src) - 1

    if before_actual_index < 0:
        src_parent.text = src.tail
        src.tail = None
    else:
        list(src_parent)[before_actual_index].tail = src.tail
        src.tail = None


    dst_parent = tree_root 
    for loc in destination[1:-1]:
        dst_parent = dst_parent.findall(loc[0])[loc[1]]
    dst_contained_name = destination[-1][0][:-2]
    dst_contained_index = destination[-1][1]

    src_parent.remove(src)
    insert_node_after_text_at_index(dst_parent, dst_contained_name, dst_contained_index, src)




''' REMOVE '''

# Parent transformation
def transform_remove_tag(curr, **kwargs):
    rem_name = kwargs['rem_name']
    rem_index = kwargs['rem_index']
    child = curr.findall(rem_name)[rem_index]
    prev_index = list(curr).index(child) -1
    if prev_index < 0:
        curr.text = child.tail
        child.tail = None
    else:
        list(curr)[prev_index].tail = curr.tail
        child.tail = None

    curr.remove(child)

# Parent transformation
def transform_remove_contained(curr, **kwargs):
    contained_name = kwargs['contained_name']
    contained_index = kwargs['contained_index']
    set_text_at_index(curr, contained_name, contained_index, None)

