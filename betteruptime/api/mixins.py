

class DynamicVariableMixin():
    '''
    Used to be able to store and keep track of dynamic variables
    '''
    _updated_vars=None

    def pre_variable_set(self, variable_name: str=None):
        '''
        Signal function that triggers before a variable actually gets set
        '''
        if not self._updated_vars:
            self._updated_vars = [variable_name]
        else:
            self._updated_vars.append(variable_name)
    
    def post_variable_set(self, variable_name: str=None):
        '''
        Signal function that triggers after a variable gets set
        '''
        pass

    def get_variable_names(self):
        '''
        Provide a list of all public variables. Excludes everything that starts with an underscore
        '''
        return [attr for attr in dir(self) if not callable(getattr(self, attr)) and not attr.startswith("_")]


    def set_variable(self, name, value, noupdate=False):
        '''
        Set a variable with a dynamic name. Can be provided with a noupdate flag
        in order to prevent the system from detecting changes

        name: Name of the variable to be assigned
        value: Value of the variable to be assigned
        noupdate: Boolean whether or not it should update the _updated_vars list
        '''
        if name in self.get_variable_names() and not noupdate:
            self.pre_variable_set(name)
        setattr(self, name, value)
        if name in self.get_variable_names() and not noupdate:
            self.post_variable_set(name)
        return self