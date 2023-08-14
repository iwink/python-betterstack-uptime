from .mixins import DynamicVariableMixin


def filter_on_attribute(objects: list, name: str, value):
    '''
    Used to be able to filter a list of objects on a specific variable

    objects: List of objects
    name: Name of the variable to be checked (str)
    value: Value to be matched
    '''
    return [x for x in objects if hasattr(x, name) and getattr(x, name) == value]
