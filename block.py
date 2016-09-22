from volume import *

class Block:
    def __init__(self):
        self.block = []
        self.directory_entry_data = []

    def get_empty_dir_entry(self):
        for i in range(0, len(self.block)):
            typeOf = type(self.block[i]);
            if (typeOf is directory_entry and not self.block[i].isUsed):
                return self.block[i];

        raise BlockWriteError("BlockWriteError: ", "No free directory entries in block.")

    def find_file_by_name(self, fileName):

        for i in range (0, len(self.block)):
            typeOf = type(self.block[i]);
            if (typeOf is directory_entry):
                if (self.block[i].directory_entry_data[1] == self.block[i].verify_and_pad(fileName)):
                    return self.block[i];


    def to_string(self):
        output = '';
        for i in range(0, len(self.block)):
            typeOf = type(self.block[i]);
            if (typeOf is directory_entry):
                output += self.block[i].to_string();
            elif (typeOf is list):
                output += ''.join(self.block[i]);
            elif (typeOf is str):
                output += self.block[i]
            else:
                pass
        return output;


class Block0(Block):
    def __init__(self):
        super().__init__()
        self.init_bitmap()
        self.block.append(self.bitmap);
        for _ in range(0, 6):
            self.block.append(directory_entry(""))

    def find_free_block_idx(self):
        for i in range(0, len(self.bitmap)):
            if (self.bitmap[i] == '-'):
                return i;

        raise NoEmptyBlocksError("No empty blocks for storage available")

    def init_bitmap(self):
        self.bitmap = ['-'] * 128
        self.bitmap[0] = '+';

    def update_bitmap_plus(self, indexes):
        for i in indexes:
            self.bitmap[i] = "+";

    def update_bitmap_minus(self, indexes):
        for i in index:
            self.bitmap[i] = "-";
