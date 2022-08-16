import os
import sys

step = int(sys.argv[1])
shift = int(sys.argv[2])
N = int(sys.argv[3])

for i in range(N):
    command = f"python preprocessing_train.py {i*step+shift} {(i+1)*step+shift} &"
    os.system(command)
    print(command)

