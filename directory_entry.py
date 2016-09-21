from error import *
class directory_entry:


    def __init__(self, name):
        self.init_entry(name);

    def verify_and_pad(self, name):
        valid = False;
        if len(name) <= 8:
            if ' ' not in name:
                return name +''.join([' '] * (9 - len(name)));
            else:
                raise NameError('Directory Entry name entered', name, 'cannot contain any space characters');
        else:
            raise NameError('Directory Entry name entered', name, 'is too long. Max 8 characters.');

    def init_entry(self, name):
        self.directory_entry_data = [];
        self.directory_entry_data.append("f:");
        self.directory_entry_data.append(self.verify_and_pad(name));
        self.directory_entry_data.append('0000');
        self.directory_entry_data.append(':');
        for i in range(0, 12):
            self.directory_entry_data.append('000 ');
        self.isUsed = False;


    def to_string(self):
        output = '';
        for i in range(0, len(self.directory_entry_data)):
            output+=self.directory_entry_data[i];
        return output;
