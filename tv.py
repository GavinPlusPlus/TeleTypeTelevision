### tv.py
###
### This file contains all code needed to download a video URL provided
### by a command line argument, downscale the image to a set resolution
### via FFMPEG, and then output the image as a character stream of 
### ASCII art.
###
### Author: GavinPlusPlus
### Date: Mar 14, 2023

import ffmpeg
import os
import yt_dlp as yt
import cv2 as opencv

class TV:

    def __new__(cls, *args, **kwargs):
        return super().__new__(cls)

    def __init__(self, x, y, fps, url):
        # Processing Flags
        self.dim_X = x
        self.dim_Y = y
        self.fps = fps
        self.yt_url = url

        # CV variables
        self.cv_init = False
        self.cv_video = None
        self.cv_frame = 0

        self.yt_opts = {
            'post_hooks': [self.dl_done],
        }

    def download_video(self):
        # Start downloading the video with yt-dlp
        print ("Starting download!")
        downloader = yt.YoutubeDL(self.yt_opts)
        downloader.download(self.yt_url)
    
    def dl_done(self, filename):
        # Rename file
        print(f"Done downloading: {self.yt_url} to {filename}")
        print("Renaming file...")
        os.rename(filename, "preOutput.webm")

        self.post_process()

        # Remove source file
        print("Removing source file")
        os.remove("preOutput.webm")
        print ("Ready for ASCII analysis...")
        
    def post_process(self):
        print ("Shrinking video down to {self.dim_X} x {self.dim_Y} via FFMPEG")
        
        # Set FFMPEG flags
        stream = ffmpeg.input("preOutput.webm")
        stream = ffmpeg.filter(stream, "fps", fps=self.fps, round="up")
        stream = ffmpeg.filter(stream, "scale", width=self.dim_X, height=self.dim_Y)
        stream = ffmpeg.hue(stream, s=0)
        stream = ffmpeg.output(stream, "output.mp4")

        # Generate Output
        os.remove("output.mp4")
        ffmpeg.run(stream)
        print ("Finished compressing the video")

    def init_cv(self):
        self.cv_video = opencv.VideoCapture("output.mp4")
        self.cv_init = True

    def convert_pixel_to_ascii(self, val):
        if (val > 220):
            return " "
        elif (val > 150):
            return "░"
        elif (val > 100):
            return "▒"
        elif (val > 60):
            return "▓"
        else:
            return "█"

    def get_ascii_frame(self):
        # Make sure video is loaded first
        if (self.cv_init == False):
            self.init_cv();            

        # Generate Text 
        output_string = ""
        transformed_ascii = []

        # Load Image
        success, frame = self.cv_video.read()

        if success:
            self.cv_frame = self.cv_frame + 1
            opencv.cvtColor(frame, opencv.COLOR_BGR2GRAY)

            # Process entire frame
            for i in frame:
                scanline = []
                for j in i:
                    scanline.append(self.convert_pixel_to_ascii(j[0]))
                transformed_ascii.append(scanline)
            
            # Generate output
            for i in transformed_ascii:
                output_string = output_string + ''.join(i)
                output_string = output_string + "\n"
            
            return output_string
        
