import os
import time
"""
tool_dir = "D:/Program Files/MuseScore 3/bin"
target_dir = "D:/Code/MidiTool/data"
target_file = "D:/Code/MidiTool/data/merged.mid"

output_file = target_file.split('.')[0] + ".png"
os.environ["PATH"] = os.environ["PATH"] + ";" + tool_dir

commend = " MuseScore3.exe -o "+ target_dir + "//" + output_file + " " + target_dir + "//" + target_file
t0 = time.time()
print(commend)
os.system(commend)
print("Time Elapsed: {:.2f} sec.".format(time.time() - t0))
"""
def sheet_function(tool_dir, input_file, output_dir):
    t0 = time.time()
    os.environ["PATH"] = os.environ["PATH"] + ";" + tool_dir
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    output_file = os.path.splitext(os.path.basename(input_file))[0] + ".png"
    commend = " MuseScore3.exe -o "+ os.path.join(output_dir, output_file) + " " + input_file
    print(commend)
    os.system(commend)
    print("Time Elapsed: {:.2f} sec.".format(time.time() - t0))
    
"""
if __name__ == "__name__":
    sheet_function("D:/Program Files/MuseScore 3/bin",
                   "D:/Code/MidiTool/data/merged.mid",
                   "D:/Code/MidiTool/data")
"""
# 4:23 -> 24.31 sec.