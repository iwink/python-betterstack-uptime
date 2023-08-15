class DynamicVariable(object):
    '''
    Class to track variables using the descriptor mechanism in python.
    Stores its data in the class that is assigned this variable using
    object id's
    '''
    def __init__(self, name: str):
        '''
        Initialize variable. The name variable should be set

        :param str name: Name of the variable
        '''
        self.name = name

    def __get__(self, obj, objtype):
        '''
        Retrieve the value of this variable using the class that has it assigned.
        Use the ID of the object as a pseudo memory address

        :param any obj: Object that has the variable
        :param any objtype: Equal to  type(obj)
        :return: Value that is set for that instance
        :rtype: any
        '''

        obj_id = obj.__get_object_id__()
        if obj_id not in obj._dynamic_variables.keys() or self.name not in obj._dynamic_variables[obj_id]:
            return None
        return obj._dynamic_variables[obj_id][self.name]

    def __set__(self, obj, val):
        '''
        Set the value of this variable using the class that has it assigned.
        Uses the ID of the object as a pseudo memory address.
        Also logs whether the variable has changed or not

        :param any obj: Object that has the variable
        :param any objtype: Equal to  type(obj)
        '''

        obj_id = obj.__get_object_id__()
        if self.name not in obj._changed_variables[obj_id]:
            if self.name in obj._dynamic_variables[obj_id].keys() and obj._dynamic_variables[obj_id][self.name] != val:
                obj._changed_variables[obj_id].append(self.name)
        obj._dynamic_variables[obj_id][self.name] = val


class DynamicVariableMixin():
    '''
    Used to be able to store and keep track of dynamic variables
    '''
    _changed_variables = {}
    _dynamic_variables = {}

    def add_tracked_property(self, property_name, property_value=None):
        '''
        Adds an instance of DynamicVariable to the entire class.
        If the variable already exists, set the value for this instance.

        :param str property_name: Name of the variable to be added
        :param any property_value: Value of the variable
        '''

        if self.__get_object_id__() not in self._changed_variables.keys():
            self._changed_variables[self.__get_object_id__()] = []
        if self.__get_object_id__() not in self._dynamic_variables.keys():
            self._dynamic_variables[self.__get_object_id__()] = {}

        if hasattr(self, property_name):
            setattr(self, property_name, property_value)
        else:
            setattr(self.__class__, property_name, DynamicVariable(property_name))
            setattr(self, property_name, property_value)

    def get_modified_properties(self):
        '''
        Returns a list of all changed variable names

        :return: List of changed variable names
        :rtype: List[str]
        '''

        return self._changed_variables[self.__get_object_id__()]

    def reset_variable_tracking(self):
        '''
        Resets the _changed_variables list to empty
        '''

        self._changed_variables[self.__get_object_id__()] = []

    def __get_object_id__(self) -> str:
        '''
        Use the builtin `id` function to get a unique, short id for this specific instance

        :return: Short ID
        :rtype: str
        '''

        return hex(id(self))
