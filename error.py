class Error(Exception):
    pass

class NameError(Error):

    def __init__(self, message):
        self.expression = "NameError: ";
        self.message = message;

class BlockWriteError(Error):
    def __init__(self, message):
        self.expression = "BlockWriteError: ";
        self.message = message;

class NoEmptyBlocksError(Error):
    def __init__(self, message):
        self.expression = "NoEmptyBlocksError': ";
        self.message = message;

class NoBlocksLeftForFile(Error):
    def __init__(self, message):
        self.expression = "NoBlocksLeftForFile: ";
        self.message = message;

class FileDoesNotExistError(Error):
    def __init__(self, message):
        self.expression = "FileDoesNotExistError: ";
        self.message = message;

class DriveFormatError(Error):
    def __init__(self):
        self.expression = "DriveFormatError: ";
        self.message = ("Please run format or reconnect before attempting to access a drive.");

class NotFileError(Error):
    def __init__(self):
        self.expression = "NotFileError: ";
        self.message = ("Directories cannot be appended to, only files.");

class DirectoryNotEmptyError(Error):
    def __init__(self):
        self.expression = "DirectoryNotEmptyError: ";
        self.message = ("Directory couldn't be deleted as it is not empty.");
