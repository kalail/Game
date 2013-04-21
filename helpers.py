

def ensure_list(method):
    def wrapper(*args, **kwargs):
        object_or_list = method(*args, **kwargs)
        if isinstance(object_or_list, list):
            return_list = object_or_list
        else:
            print 'Converted in decorator'
            return_list = [object_or_list]
        return return_list
     
    return wrapper