import subprocess
import os

# Directory where mini videos are located
mini_loc = "/Users/chrisomlor/Video/mp4/"

# Get List of files in directory of mini files
mini_video = os.listdir("/Users/chrisomlor/Video/mp4/")

# Array of parameters to build movie merge command
# mp4box - Program used to build concatenation
# -tmp - Parameter to override temp directory location
# /Users/chrisomlor/Video/mp4/temp/ - Location to use as a temp directory
file_list = ["mp4box", "-tmp", "/Users/chrisomlor/Video/mp4/temp/", ]

# Boolean for first file name to use -add <filename> parameter
# Every other parameter will be -cat <filename>
first = True

# Iterate through the list of files in directory and append
# appropriate commands to the list
for f in mini_video:
    the_file = ""
    if f.endswith(".mp4"):
        if first:
            file_list.append("-add")
            the_file = mini_loc
            the_file += f
            file_list.append(the_file)
            first = False
        else:
            file_list.append("-cat")
            the_file = mini_loc
            the_file += f
            file_list.append(the_file)

# Make string for output file location and filename and append
# to the end of the list
output = mini_loc
output += "output.mp4"
file_list.append(output)

# Execute the command through a subprocess call
subprocess.call(file_list)
