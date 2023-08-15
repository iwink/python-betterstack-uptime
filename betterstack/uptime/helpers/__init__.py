from typing import List


def filter_on_attribute(objects: list, name: str, value: any) -> List[any]:
    '''
    Used to be able to filter a list of objects on a specific variable

    :param list objects: Objects to be filtered
    :param str name: Attribute to be filtered
    :param any value: Value to be filtered
    :return: List of matching objects
    :rtype: list
    '''

    return [x for x in objects if hasattr(x, name) and getattr(x, name) == value]
