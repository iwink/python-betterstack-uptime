class DynamicVariable(object):
    def __init__(self, name='var'):
        self.name = name

    def __get__(self, obj, objtype):
        if hex(id(obj)) not in obj._dynamic_variables.keys() or self.name not in obj._dynamic_variables[hex(id(obj))]:
            return None
        return obj._dynamic_variables[hex(id(obj))][self.name]

    def __set__(self, obj, val):
        obj_id = hex(id(obj))
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

        property_name: str  Name of the variable to be added
        property_value: any Value of variable
        '''
        if hex(id(self)) not in self._changed_variables.keys():
            self._changed_variables[hex(id(self))] = []
        if hex(id(self)) not in self._dynamic_variables.keys():
            self._dynamic_variables[hex(id(self))] = {}


        if hasattr(self, property_name):
            setattr(self, property_name, property_value)
        else:
            setattr(self.__class__, property_name, DynamicVariable(property_name))
            setattr(self, property_name, property_value)


    def get_modified_properties(self):
        '''
        Returns a list of all changed variable names
        '''
        return self._changed_variables[hex(id(self))]

    def reset_variable_tracking(self):
        '''
        Resets the _changed_variables list to empty
        '''
        self._changed_variables[hex(id(self))] = []