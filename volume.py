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
                to_write = str_to_write[(512*i):(512*(i+1))];
                self.blocks[idxs[i]].block.append(to_write)
                self.drive.write_block(idxs[i], self.pad_space(to_write));

        def delfile(self, name, dir_block):
            #delete data
            dir_entry = dir_block.find_file_by_name(name);
            blocks_idxs = dir_entry.get_assigned_blocks();
            for i in range(0, len(blocks_idxs)):
                self.blocks[blocks_idxs[i]].wipe_self();
                self.write(self.blocks[blocks_idxs[i]].to_string(), [blocks_idxs[i]]);

            #reset dir_entry
            dir_entry.reset()
            #reset bitmap
            self.blocks[0].update_bitmap_minus(blocks_idxs);

            #write to disk
            self.write(self.blocks[0].to_string(), [0]);
            self.write(dir_block.to_string(), [self.blocks.index(dir_block)]);

        def deldir(self, name, dir_block):
            dir_entry = dir_block.find_file_by_name(name);
            blocks_idxs = dir_entry.get_assigned_blocks();
            dir_is_empty = True;
            for i in range(0, len(blocks_idxs)):
                if (self.blocks[blocks_idxs[i]].is_empty() == False):
                    dir_is_empty = False;
                    break;

            if (dir_is_empty == False):
                raise DirectoryNotEmptyError();
            else:
                for i in range(0, len(blocks_idxs)):
                    self.blocks[blocks_idxs[i]].wipe_self()
                    self.write(self.blocks[blocks_idxs[i]].to_string(), [blocks_idxs[i]]);

            #reset dir_entry
            dir_entry.reset()
            #reset bitmap
            self.blocks[0].update_bitmap_minus(blocks_idxs);

            #write to disk
            self.write(self.blocks[0].to_string(), [0]);
            self.write(dir_block.to_string(), [self.blocks.index(dir_block)]);



            #reset all blocks

            #reset dir Entry

            #update bitmap


        def parse_path(self, path):
            #Is root
            if (path == '/'):
                return (self.blocks[0], '');

            split_path = path.split('/');

            if(len(split_path) < 2):
                raise IndexError

            num_paths = len(split_path) - 1;
            #Only one level down [in root]
            if(num_paths == 1):
                return (self.blocks[0], split_path[1]);
            else:
                return self.dig_through_path(split_path);

        def dig_through_path(self, split_path):
            current_blocks = [self.blocks[0]];
            for i in range(1, len(split_path) - 1 ):
                next_dir_to_find = split_path[i];
                found = False;
                for i in range(0, len(current_blocks)):
                    try:
                        dir_entry = current_blocks[i].find_file_by_name(next_dir_to_find);
                        found = True;
                        break;
                    except FileDoesNotExistError:
                        pass
                if(found == False):
                    raise FileDoesNotExistError(next_dir_to_find + " does no exist.")

                if(dir_entry.has_block_allocated() == False):
                    #init dir
                    block = self.assign_block_to_dir(dir_entry);
                    return(block, split_path[len(split_path) - 1]);
                else:
                    assigned_block_idxs = dir_entry.get_assigned_blocks();
                    current_blocks = [];
                    for i in range(0, len(assigned_block_idxs)):
                        current_blocks.append(self.blocks[assigned_block_idxs[i]]);

            return (current_blocks[len(current_blocks) - 1], split_path[len(split_path) - 1]);


        def assign_block_to_dir(self, dir_entry):
            assigned_blocks = self.assign_blocks(dir_entry, self.blocks[0].find_free_block_idx(1), 512);
            dir_entry.set_size(512);
            assigned_blocks[0].init_directory();
            self.write_all_previous_blocks(self.blocks.index(assigned_blocks[0]));
            return assigned_blocks[0];


        def write_all_previous_blocks(self, up_to_block):
            for i in range(0, up_to_block + 1):
                self.write(self.blocks[i].to_string(), [i])

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
            dir_entry = dir_block.find_file_by_name(fileName);
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
            self.write_all_previous_blocks(self.blocks.index(dir_block));

        def mkfile(self, fileName, dir_block):
            if ' ' not in fileName:
                try:
                    emptyDirectoryEntry = dir_block.get_empty_dir_entry()
                    emptyDirectoryEntry.directory_entry_data[1] = emptyDirectoryEntry.verify_and_pad(fileName);
                    self.write_all_previous_blocks(self.blocks.index(dir_block))
                except Error as e:
                    raise e;
            else:
                raise NameError("File name can't contain spaces.")

        def append(self, fileName, data, dir_block):
                    #find directory entry with a fileName
                dir_entry = dir_block.find_file_by_name(fileName);
                print (dir_entry)
                if dir_entry.directory_entry_data[0] == 'd:':
                    raise NotFileError()
                #find latest block with file data OR assign a block if no block assigned
                if (dir_entry.has_block_allocated()):
                    #get latest empty block
                    #save in free_block_idx var
                    block_idxs = dir_entry.get_assigned_blocks()
                    last_block_idx = block_idxs[len(block_idxs) - 1];
                    #read block
                    existing_data = self.blocks[last_block_idx].block[0];
                    space_left = 512-len(existing_data);

                    existing_data += data;
                    block_idxs = self.blocks[0].find_free_block_idx(((len(data) - space_left) // 512 )+ 1);
                    blocks = self.assign_blocks(dir_entry, block_idxs, len(existing_data))
                    block_idxs.insert(0, last_block_idx);
                    self.write(existing_data, block_idxs);
                    self.write_all_previous_blocks(block_idxs[len(block_idxs) - 1]);

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
                        self.write_all_previous_blocks(free_block_idxs[len(free_block_idxs) - 1]);



        def assign_blocks(self, dir_entry, free_block_idxs, data_len):
            dir_entry.assign_blocks(free_block_idxs, data_len);
            free_blocks = [];
            for i in range (0, len(free_block_idxs)):
                free_blocks.append(self.blocks[free_block_idxs[i]])
            self.blocks[0].update_bitmap_plus(free_block_idxs);
            return free_blocks;
