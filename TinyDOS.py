from error import *
from volume import *
import readline

class TinyDOS:

    def __init__(self):
        self.input = input()
        while(self.input != 'quit'):
            self.parse_input()
            self.input = input()

    def parse_input(self):
        try:
            splitInput =  self.input.split(' ')
            if(splitInput[0] == 'format'):
                #do something
                self.format(splitInput[1])
            elif(splitInput[0] == 'mkdir'):
                if (not hasattr(self, 'volume')):
                    raise DriveFormatError()
                self.mkdir(splitInput[1]);
            elif(splitInput[0] == 'reconnect'):
                self.reconnect(splitInput[1])
            elif(splitInput[0] == 'ls'):
                if (not hasattr(self, 'volume')):
                    raise DriveFormatError()
                self.ls(splitInput[1]);
            elif(splitInput[0] == 'mkfile'):
                if (not hasattr(self, 'volume')):
                    raise DriveFormatError()
                self.mkfile(splitInput[1]);
            elif(splitInput[0] == 'append'):
                if (not hasattr(self, 'volume')):
                    raise DriveFormatError()
                self.append(splitInput[1], splitInput[2]);
            elif(splitInput[0] == 'print'):
                if (not hasattr(self,'volume')):
                    raise DriveFormatError()
                self.print(splitInput[1]);
            elif(splitInput[0] == 'delfile'):
                if (not hasattr(self, 'volume')):
                    raise DriveFormatError()
                self.delfile(splitInput[1]);
            elif(splitInput[0] == 'deldir'):
                if (not hasattr(self, 'volume')):
                    raise DriveFormatError()
                self.deldir(splitInput[1]);
            elif(splitInput[0] == 'quit'):
                #graceful cleanup if needed otherwise delete this
                pass
            else:
                print("Error: Command not recognised")
        except Error as e:
            print(e.expression, e.message);
        except IndexError:
            print("Error: Please use full path when referencing file/dirs. e.g. A file called 'file' in the root directory will be referenced by '/file'.")

    def deldir(self, file_path):
        block_and_name = self.volume.parse_path(file_path);
        self.volume.deldir(block_and_name[1], block_and_name[0]);

    def delfile(self, file_path):
        block_and_name = self.volume.parse_path(file_path);
        self.volume.delfile(block_and_name[1], block_and_name[0]);

    def ls(self, dir_path):
        block_and_name = self.volume.parse_path(dir_path);
        self.volume.ls(block_and_name[1], block_and_name[0]);

    def print(self, file_path):
        block_and_name = self.volume.parse_path(file_path);
        self.volume.print(block_and_name[1], block_and_name[0]);

    def mkdir(self, dir_path):
        block_and_name = self.volume.parse_path(dir_path);
        print(block_and_name[0].to_string())
        self.volume.mkdir(block_and_name[1], block_and_name[0]);

    def reconnect(self, volumeName):
        self.volume = Volume(volumeName);
        self.volume.reconnect()

    def format(self, volumeName):
        self.volume = Volume(volumeName)
        self.volume.format()

    def mkfile(self, file_path):
        try:
            block_and_name = self.volume.parse_path(file_path)
            self.volume.mkfile(block_and_name[1], block_and_name[0])
        except Error as e:
            print(e.expression, e.message);

    def append(self, file_path, data):
        block_and_name = self.volume.parse_path(file_path);
        self.volume.append(block_and_name[1], data, block_and_name[0]);

if __name__ == '__main__':
    tinydos = TinyDOS()
