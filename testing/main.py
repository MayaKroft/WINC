def get_none():
    return None

def go_deeper(a):
    embedded_list = []
    if type(a) == list:
        for item in a:
            if isinstance(item, dict):
                ext0 = go_deeper(item)
            elif isinstance (item, list):
                ext1 = go_deeper(item)
            else:
                embedded_list.append(item)
    elif type(a) == dict:
        for item in a.items():
            if isinstance(item[1], dict):
                ext2 = go_deeper(item[1])
            elif isinstance (item[1], list):
                ext3 = go_deeper(item[1])
            else:
                embedded_list.append(item[1])
    try:
        embedded_list.extend(ext0)
    except:
        pass
    try:
        embedded_list.extend(ext1)
    except:
        pass
    try:
        embedded_list.extend(ext2)
    except:
        pass
    try:
        embedded_list.extend(ext3)
    except:
        pass
    return embedded_list
    

def flatten_dict(dictionary):
    flat_list = []
    
    for item in dictionary.items():
        if isinstance(item[1], dict):
            flat_list.extend(go_deeper(item[1]))
        elif isinstance (item[1], list):
            flat_list.extend(go_deeper(item[1]))
        else:
            flat_list.append(item[1])
    print(flat_list)
    return flat_list

