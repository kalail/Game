

def ensure_list(method):
	def wrapper(*args, **kwargs):
		object_or_list = method()
		if isinstance(object_or_list, list):
			return_list = object_or_list
		else:
			return_list = [object_or_list]
		return return_list
	 
	return wrapper