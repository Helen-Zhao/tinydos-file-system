import error

class directory_entry:


    def __init__(self, name):
        self.error_check(name);
        self.populate_entry(name);


        self.directory_entry_data = {};
        self.directory_entry_data['0'] = "d:"
        self.directory_entry_data['1'] = name + " ";

    @catch_exception_decorator
    def error_check(self, name):
            if len(name) > 8:
                raise NameError('Directory Entry name entered', name, 'is too long. Max 8 characters.');

    def catch_exception_decorator(function):
       def decorated_function:
          try:
             function()
         except Error:
             raise Error
       return decorated_function
