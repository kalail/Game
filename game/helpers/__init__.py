

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
    if m == 0:
        return (0, 0)
    normalized = (vector[0]/m, vector[1]/m)
    return normalized


def get_direction(start, end):
    delta_x = end[0] - start[0]
    delta_y = end[1] - start[1]
    return normalize((delta_x, delta_y))
