from drive import *
from directory_entry import *
from error import *
from block import *
from directory import *

class Volume:

        def __init__(self, volumeName):
            self.volumeName = volumeName;
            self.drive = Drive(volumeName)
            self.blocks = [];

        def format(self):
            self.drive.format()

            #This this tracks all the blocks
            self.blocks.append(Block0());
            for i in range(0, 127):
                self.blocks.append(Block());

            blockInfoToWrite = self.blocks[0].to_string();
            self.write(blockInfoToWrite, [0])

        def write(self, str_to_write, idxs):
            for i in range(0, len(idxs)):
                self.drive.write_block(idxs[i],self.pad_space(str_to_write[(512*i):(512*(i+1))]));

        def print(self, file_path):
            dir_entry = self.blocks[0].find_file_by_name(file_path);
            blocks = dir_entry.get_assigned_blocks();
            output = '';
            for i in range(0, len(blocks)):
                output += self.drive.read_block(blocks[i]);

        def pad_space(self, str_to_pad):
            return str_to_pad + ''.join([' '] * (512 - len(str_to_pad)));

        def reconnect(self):
            self.drive.reconnect();
            self.blocks.append(Block0(self.drive.read_block(0)));
            for i in range(1, 128):
                data = self.drive.read_block(i);
                self.blocks.append(Block(data));

        def mkdir(self, dir_path):
            if '/' not in dir_path:
                dir_entry = self.blocks[0].get_empty_dir_entry();
                dir_entry.directory_entry_data[1] = dir_entry.verify_and_pad(dir_path);
                dir_entry.directory_entry_data[0] = 'd:';
                blockInfoToWrite

        def mkfile(self, fileName):
            if '/' not in fileName:
                if ' ' not in fileName:
                    try:
                        emptyDirectoryEntry = self.blocks[0].get_empty_dir_entry()
                        emptyDirectoryEntry.directory_entry_data[1] = emptyDirectoryEntry.verify_and_pad(fileName);
                        blockInfoToWrite = self.blocks[0].to_string();
                        self.write(blockInfoToWrite, [0])
                    except Error as e:
                        raise e;
                else:
                    raise NameError("File name can't contain spaces.")

        def append(self, fileName, data):
            if '/' not in fileName:
                    #find directory entry with a fileName
                dir_entry = self.blocks[0].find_file_by_name(fileName);
                #find latest block with file data OR assign a block if no block assigned
                if (dir_entry.has_block_allocated()):
                    #get latest empty block
                    #save in free_block_idx var
                    pass

                else:
                    #assign block
                    free_block_idxs = set()
                    for _ in range(0, (len(data) // 512) + 1):
                        free_block_idxs.add(self.blocks[0].find_free_block_idx());
                        blocks = self.assign_blocks(dir_entry, list(free_block_idxs), len(data));

                #add data values to the end of the block
                for i in range(0, len(blocks)):
                    block = blocks[i];
                    block.block.append(data)
                    blockInfoToWrite = block.to_string()
                    self.write(blockInfoToWrite, free_block_idxs);
                    self.write(self.blocks[0].to_string(), [0]);


        def assign_blocks(self, dir_entry, free_block_idxs, data_len):
            dir_entry.assign_blocks(free_block_idxs, data_len);
            free_blocks = [];
            for i in range (0, len(free_block_idxs)):
                free_blocks.append(self.blocks[free_block_idxs[i]])
            self.blocks[0].update_bitmap_plus(free_block_idxs);
            return free_blocks;
