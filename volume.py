from drive import *
from directory_entry import *
from error import *
from block import *

class Volume:

        def __init__(self, volumeName):
            self.drive = Drive(volumeName)
            self.drive.format()

        def format(self):
            #This this tracks all the blocks
            self.blocks = []
            self.blocks.append(Block0());
            for i in range(0, 127):
                self.blocks.append(Block());

            blockInfoToWrite = self.blocks[0].to_string();
            self.write(blockInfoToWrite, 0)

        def write(self, str_to_write, n):
            length = len(str_to_write)
            if (length <= 512):
                self.drive.write_block(n, self.pad_space(str_to_write));
            else:
                noBlocks = length / 512;
                for i in range(0, noBlocks):
                    self.drive.write_block(self.blocks[0].find_free_block,self.pad_space(str_to_write[(512*i):(512*(i+1))]));

        def pad_space(self, str_to_pad):
            return str_to_pad + ''.join([' '] * (512 - len(str_to_pad)));

        def mkfile(self, fileName):
            if '/' not in fileName:
                if ' ' not in fileName:
                    try:
                        emptyDirectoryEntry = self.blocks[0].get_empty_dir_entry()
                        emptyDirectoryEntry.directory_entry_data[1] = emptyDirectoryEntry.verify_and_pad(fileName);
                        blockInfoToWrite = self.blocks[0].to_string();
                        self.write(blockInfoToWrite, 0)

                    except Error as e:
                        raise e;
                else:
                    raise NameError("NameError: ", "File name can't contain spaces.")
