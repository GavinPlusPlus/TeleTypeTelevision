### Main.py
### Executable for the TV class

import tv
import time
import sys

newTV = tv.TV(120, 44, 30, "https://www.youtube.com/watch?v=dQw4w9WgXcQ")

# Check for download skip
if (len(sys.argv) > 1):
    print ("Skipping download! Playing cached video")
else:
    newTV.download_video()

wipe = "\033[F\033[F\033[F\033[F\033[F\033[F\033[F\033[F\033[F\033[F\033[F\033[F\033[F\033[F\033[F\033[F\033[F\033[F\033[F\033[F\033[F\033[F\033[F\033[F\033[F\033[F\033[F\033[F\033[F\033[F\033[F\033[F\033[F\033[F\033[F\033[F\033[F\033[F\033[F\033[F\033[F\033[F\033[F\033[F\033[F\033[F\033[Fv"

# Timers for drawing
start_draw = end_draw = diff_draw = total_draw = sleep_time = 0
fps_time = 1 / newTV.fps 

for i in range (0, 2000):    
    print (wipe)
    start_draw = time.perf_counter()

    # Render
    print(newTV.get_ascii_frame())
    print(f"Render: {newTV.get_render_time()} Draw: {diff_draw} Total: {total_draw} Sleep: {sleep_time}")

    # Calculate Time
    end_draw = time.perf_counter()
    diff_draw = end_draw - start_draw
    total_draw = newTV.get_render_time() + diff_draw
    sleep_time = fps_time - total_draw

    # Only sleep if time is positive
    if (sleep_time > 0):
        time.sleep(sleep_time)
    