import xml.etree.ElementTree as ET

'''
Takes locations as an array and returns the node indicated
by the final location in the array.
split_path is [(path, occurence), ...]
'''
def get_node_from_path(root, split_path):
    # Root is first location so can be skipped
    split_path = split_path[1:]
    curr = root
    for single_dir in split_path:
        dir_name = split_path[0]
        index = split_path[1]

        curr = root.findall(dir_name)[index]
    return curr


'''
Same as above but for use with commands in which the final
directory of the path is not another tag, but an attribute
(preceded by '@'), or a text/comment block, e.g. 'text()'
'''
def get_parent_from_path(root, split_path):
    pass
