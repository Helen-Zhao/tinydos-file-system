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
                pass
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
                pass
            elif(splitInput[0] == 'deldir'):
                if (not hasattr(self, 'volume')):
                    raise DriveFormatError()
                pass
            elif(splitInput[0] == 'quit'):
                #graceful cleanup if needed otherwise delete this
                pass
            else:
                print("Error: Command not recognised")
        except Error as e:
            print(e.expression, e.message);


    def print(self, file_path):
        self.volume.print(file_path);

    def mkdir(self, dir_path):
        self.volume.mkdir(dir_path);

    def reconnect(self, volumeName):
        self.volume = Volume(volumeName);
        self.volume.reconnect()

    def format(self, volumeName):
        self.volume = Volume(volumeName)
        self.volume.format()

    def mkfile(self, fileName):
        try:
            self.volume.mkfile(fileName)
        except Error as e:
            print(e.expression, e.message);

    def append(self, fileName, data):
        self.volume.append(fileName, data);

if __name__ == '__main__':
    tinydos = TinyDOS()
