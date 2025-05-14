import os

def is_rel_path(full:str, parent:str) -> bool:
    full = os.path.normpath(full)
    parent = os.path.normpath(parent)
    return full.startswith(parent)

def path_depth(path:str) -> int:
    path = os.path.normpath(path)
    return len(path.split(os.sep)) -1

def in_depth(full:str, parent:str=None, depth:int=-1) -> bool:

    dep = path_depth(full)

    if parent:
        dep -= path_depth(parent)
        if not is_rel_path(full, parent):
            return False
    
    if depth!=-1:
        if dep>depth:
            return False
    
    return True