import volume
import sys

class TinyDOS:



    @catch_exception_decorator
    def __init__(self):
        command = raw_input('TinyDOS started. Please enter commands:')

    @catch_exception_decorator
    def format(self, volumeName):
        self.volumeName = Volume()
        self.volumeName.format()


    def catch_exception_decorator(function):
       def decorated_function:
          try:
             function()
         except Error:
             raise Error
       return decorated_function
