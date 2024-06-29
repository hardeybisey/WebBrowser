def tree_to_list(tree, _list):
    "Convert a tree to a list."
    _list.append(tree)
    for child in tree.children:
        tree_to_list(child, _list)
    return _list

