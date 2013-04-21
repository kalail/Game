

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


def normalize(vector):
    m = (vector[0]**2 + vector[1]**2)**0.5
    normalized = (vector[0]/m, vector[1]/m)
    return normalized