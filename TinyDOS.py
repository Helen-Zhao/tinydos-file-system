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
        splitInput =  self.input.split(' ')
        if(splitInput[0] == 'format'):
            #do something
            self.format(splitInput[1])
        elif(splitInput[0] == 'mkdir'):
            pass
        elif(splitInput[0] == 'reconnect'):
            pass
        elif(splitInput[0] == 'ls'):
            pass
        elif(splitInput[0] == 'mkfile'):
            self.mkfile(splitInput[1]);
        elif(splitInput[0] == 'append'):
            self.append(splitInput[1], splitInput[2]);
        elif(splitInput[0] == 'print'):
            pass
        elif(splitInput[0] == 'delfile'):
            pass
        elif(splitInput[0] == 'deldir'):
            pass
        elif(splitInput[0] == 'quit'):
            #graceful cleanup if needed otherwise delete this 
            pass
        else:
            print("Error: Command not recognised")

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
