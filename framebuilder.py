### framebuilder.py
###
### This class contains the code needed to build to build a frame of
### a television "field"
###
### Author: GavinPlusPlus
### Date: Mar 15, 2023

class FrameBuilder:

    def __new(cls, *args, **kwargs):
        return super().__new__(cls)
    
    def __init__(self, pre_processed_frame):
        self.frame = pre_processed_frame
        self.last_output_frame = ""

    def convert_pixel_to_ascii(self, val):
        if (val > 224):
            return " "
        elif (val > 153):
            return "░"
        elif (val > 102):
            return "▒"
        elif (val > 51):
            return "▓"
        else:
            return "█"
        
    def build_frame(self):
        transformed_ascii = []

        # Loop through each 
        for i in self.frame:
            scanlines = []
            for j in i:
                scanlines.append(self.convert_pixel_to_ascii(j[0]))
            scanlines.append("\n")
            transformed_ascii.append(scanlines)

        output = ""
        for i in transformed_ascii:
            output = output + "".join(i)

        return output