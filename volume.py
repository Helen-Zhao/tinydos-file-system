import drive
import directory_entry
import exception_catcher

class Volume:

        def __init__(self, volumeName):
            self.drive = Drive(volumeName)
            self.drive.format()

        def format(self):
            #This dictionary stores the data for block0
            self.block0 = {}

            self.init_bitmap()
            self.block0['0'] = self.bitmap;
            self.block0['1'] = directory_entry()
            self.block0['2'] = directory_entry()
            self.block0['3'] = directory_entry()
            self.block0['4'] = directory_entry()
            self.block0['5'] = directory_entry()
            self.block0['6'] = directory_entry()

            var blockInfoToWrite = ""
            for i in range 0 to 7:
                blockInfoToWrite.append(''.join(self.block0[i]));

            #Create 6 directory entries
            for _ in range(0 to 6):


            self.drive.write_block(0, )


        def init_bitmap(self):
            self.bitmap = []
            bitmap.append("+")
            for _ in range(1, 128):
                bitmap.append("-")

        def update_bitmap_plus(self, *indexes):
            for i in index:
                self.bitmap[i] = "+";


        def update_bitmap_minus(self, *indexes):
            for i in index:
                self.bitmap[i] = "-";
