from error import *
class directory_entry:


    def __init__(self, *directory_entry_string):
        self.directory_entry_data = [];
        print('destr', directory_entry_string);
        if(len(directory_entry_string) > 0):
            self.parse_entry(directory_entry_string[0]);

        else:
            print("in init_entry")
            self.init_entry();


    def parse_entry(self, string):
        self.directory_entry_data.append(string[0:2]);
        self.directory_entry_data.append(string[2:11]);
        self.directory_entry_data.append(string[11:15]);
        self.directory_entry_data.append(string[15:16]);
        count = 16
        for i in range(0, 12):
            self.directory_entry_data.append(string[count:(count + 4)]);
            count += 4;

        print('str:', string, 'created:', self.to_string())

    def get_assigned_blocks(self):
        blocks = [];
        for i in range(4, len(directory_entry_data)):
            string_block = self.directory_entry_data[i];
            blocks.append(int(string_block[0:4]));
            return blocks;

    def verify_and_pad(self, name):
        valid = False;
        if len(name) <= 8:
            if ' ' not in name:
                return name +''.join([' '] * (9 - len(name)));
            else:
                raise NameError('Directory Entry name entered ' + name + 'cannot contain any space characters');
        else:
            raise NameError('Directory Entry name entered ' + name + ', is too long. Max 8 characters.');

    def init_entry(self):
        self.directory_entry_data.append("f:"); #idx 0
        self.directory_entry_data.append(self.verify_and_pad("")); #idx 1
        self.directory_entry_data.append('0000'); #idx 2
        self.directory_entry_data.append(':'); #idx 3
        for i in range(0, 12):
            self.directory_entry_data.append('000 '); #idx 4 - 16
        self.isUsed = False;

    def has_block_allocated(self):
        if(self.directory_entry_data[2] == '0000' and self.directory_entry_data[4] == '000 '):
            return False;
        elif(self.directory_entry_data[4] is not '000 '):
            return True;

    def assign_blocks(self, block_idxs, data_len):
        #Get first free block for file
        for i in range(4, len(self.directory_entry_data)):
            if (self.directory_entry_data[i] == '000 '):
                dir_entry_block = i;
                break;

        self.directory_entry_data[2] = self.format_size(data_len);

        for j in range(0, len(block_idxs)):
            self.directory_entry_data[dir_entry_block] = self.format_block_num(block_idxs[j]);
            print(block_idxs)
            print(self.format_block_num(block_idxs[j]));
            dir_entry_block += 1;
            if (dir_entry_block > len(self.directory_entry_data)):
                raise NoBlocksLeftForFile("This file has no blocks left to assign - All 12 have been used.");

    def format_size(self, size):
        return ''.join(['0'] * (4 - len(str(size)))) + str(size);


    def format_block_num(self, block_num):
        #pad str_num
        return ''.join(['0'] * (3 - len(str(block_num)))) + str(block_num) + ' ';

    def to_string(self):
        output = '';
        for i in range(0, len(self.directory_entry_data)):
            output += self.directory_entry_data[i];
        return output;
