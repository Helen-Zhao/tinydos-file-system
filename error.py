class Error(Exception):
    pass

class NameError(Error):

    def __init__(self, message):
        self.expression = "NameError: ";
        self.message = message;

class BlockWriteError(Error):
    def __init__(self, message):
        self.expression = "NameError: ";
        self.message = message;
