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
import time
import yt_dlp as yt
import cv2 as opencv
import framebuilder

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

        # Timing variables
        self.time_start_build = 0
        self.time_end_build = 0
        self.time_diff = 0

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

    def get_render_time(self):
        return self.time_diff

    def get_ascii_frame(self):
        # Start Timer
        self.time_start_build = time.perf_counter()

        # Make sure video is loaded first
        if (self.cv_init == False):
            self.init_cv();            
        
        # Load Image
        success, frame = self.cv_video.read()

        # Use FrameBuilder to Process Image 
        if success:
            opencv.cvtColor(frame, opencv.COLOR_BGR2GRAY)
            result = framebuilder.FrameBuilder(frame).build_frame()
            self.time_end_build = time.perf_counter()

            self.time_diff = self.time_end_build - self.time_start_build

            return result