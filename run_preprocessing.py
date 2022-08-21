import os
import sys

shift = int(sys.argv[1])
step = int(sys.argv[2])
N = int(sys.argv[3])
mode = sys.argv[4]

for i in range(N):
    if mode == "train":
        command = f"python preprocessing.py {i*step+shift} {(i+1)*step+shift} False &"
    else:
        energy = sys.argv[5]
        command = f"python preprocessing.py {i*step+shift} {(i+1)*step+shift} True {energy} &"
    os.system(command)
    print(command)

