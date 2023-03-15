### Main.py
### Executable for the TV class

import tv
import time
import sys

newTV = tv.TV(90, 44, 15, "https://www.youtube.com/watch?v=FtutLA63Cp8")

# Check for download skip
if (len(sys.argv) > 1):
    print ("Skipping download! Playing cached video")
else:
    newTV.download_video()

wipe = "\033[F\033[F\033[F\033[F\033[F\033[F\033[F\033[F\033[F\033[F\033[F\033[F\033[F\033[F\033[F\033[F\033[F\033[F\033[F\033[F\033[F\033[F\033[F\033[F\033[F\033[F\033[F\033[F\033[F\033[F\033[F\033[F\033[F\033[F\033[F\033[F\033[F\033[F\033[F\033[F\033[F\033[F\033[F\033[F\033[F\033[Fv"

for i in range (0, 2000):    
    print(newTV.get_ascii_frame())
    time.sleep(0.06)
    print(wipe)
    