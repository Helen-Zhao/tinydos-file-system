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
                self.drive.write_block(idxs[i], self.pad_space(str_to_write[(512*i):(512*(i+1))]));

        def parse_path(self, path):
            if (path == '/'):
                return (self.blocks[0], '');

            split_path = path.split('/');
            num_paths = len(split_path) - 1;

            if(num_paths == 1):
                #in root_dir_entry
                return (self.blocks[0], split_path[1]);
            else:
                root_dir_entry = self.blocks[0].find_file_by_name(split_path[1]);
                if root_dir_entry.has_block_allocated():

                    current_dir_entry = root_dir_entry;
                    for i in range(2, num_paths)
                        block_idxs = current_dir_entry.get_assigned_blocks()
                        found = False;
                        for i in range(0, len(block_idxs)):
                            block = self.blocks[block_idxs[i]]
                            try:
                                current_dir_entry = block.find_file_by_name(split_path[i]);
                                latest_block = block;
                                found = True;
                                break;
                            except FileDoesNotExistError:
                                pass
                        if not found:
                            raise FileDoesNotExistError("File or Directory in path " + split_path[i] + " does not exist.")

                    return(latest_block, split_path[num_paths]);
                        #if file dir entry doesn't exist, throw error
                else:
                    #allocate block to dir, create file


        def ls(self, dir_name, parent_dir_block):
            if dir_name is '':
                print(self.blocks[0].to_string_ignore_empty());
            else:
                dir_entry = parent_dir_block.find_file_by_name(dir_name);
                blocks_idxs = dir_entry.get_assigned_blocks()
                output = '';
                for i in range(0, len(blocks_idxs)):
                    output += self.blocks[blocks_idxs[i]].to_string_ignore_empty();

                print(output);

        def print(self, fileName, dir_block):
            dir_entry = self.blocks[0].find_file_by_name(file_path);
            blocks = dir_entry.get_assigned_blocks();
            output = '';
            for i in range(0, len(blocks)):
                if i == len(blocks) - 1:
                    output += self.drive.read_block(blocks[i]).rstrip();
                else:
                    output += self.drive.read_block(blocks[i]);

            print(output);

        def pad_space(self, str_to_pad):
            return str_to_pad + ''.join([' '] * (512 - len(str_to_pad)));

        def reconnect(self):
            self.drive.reconnect();
            self.blocks.append(Block0(self.drive.read_block(0)));
            for i in range(1, 128):
                data = self.drive.read_block(i);
                self.blocks.append(Block(data));

        def mkdir(self, dir_name, dir_block):
            dir_entry = dir_block.get_empty_dir_entry();
            dir_entry.change_to_directory(dir_name);
            self.write(dir_block.to_string(), [self.blocks.index(dir_block)]);

        def mkfile(self, fileName, dir_block):
            print(fileName, dir_block)
            if ' ' not in fileName:
                try:
                    emptyDirectoryEntry = dir_block.get_empty_dir_entry()
                    emptyDirectoryEntry.directory_entry_data[1] = emptyDirectoryEntry.verify_and_pad(fileName);
                    blockInfoToWrite = dir_block.to_string();
                    self.write(blockInfoToWrite, [self.blocks.index(dir_block)])
                except Error as e:
                    raise e;
            else:
                raise NameError("File name can't contain spaces.")

        def append(self, fileName, data, dir_block):
                    #find directory entry with a fileName
                dir_entry = dir_block.find_file_by_name(fileName);
                #find latest block with file data OR assign a block if no block assigned
                if (dir_entry.has_block_allocated()):
                    #get latest empty block
                    #save in free_block_idx var
                    block_idxs = dir_entry.get_assigned_blocks()
                    last_block_idx = block_idxs[len(block_idxs) - 1];

                    #read block
                    existing_data = self.drive.read_block(last_block_idx).rstrip();
                    space_left = 512-len(existing_data);

                    existing_data += data;
                    block_idxs = self.blocks[0].find_free_block_idx(((len(data) - space_left) // 512 )+ 1);
                    block_idxs.insert(0, last_block_idx);
                    self.write(existing_data, block_idxs);

                else:
                    #assign block
                    free_block_idxs = []
                    free_block_idxs = self.blocks[0].find_free_block_idx((len(data) // 512) + 1);

                    blocks = self.assign_blocks(dir_entry, free_block_idxs, len(data));

                    #add data values to the end of the block
                    for i in range(0, len(blocks)):
                        block = blocks[i];
                        block.block.append(data);
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
