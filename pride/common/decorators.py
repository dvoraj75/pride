

def global_object(original_class: type) -> type:
    """
    Class decorator to add instance of original class to global dict.

    Args:
        original_class(type): class to decorate

    Returns:
        type: decorated class
    """
    def __new__(cls, *args, **kwargs):
        global_objects = globals()['global_objects_']
        global_objects[cls.__name__] = original_new(cls, *args, **kwargs)
        return global_objects[cls.__name__]

    original_new = original_class.__new__
    original_class.__new__ = __new__
    return original_class
