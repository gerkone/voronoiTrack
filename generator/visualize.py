import argparse
import matplotlib.pyplot as plt
import numpy as np
import os

def read_points(data):
    xs = []
    ys = []
    for q in data:
        xs.append(q[0])
        ys.append(q[1])
    return xs, ys

def plot(data, seed, width):
    xs, ys = read_points(data)

    fig, axs = plt.subplots(1, 1, constrained_layout=True)
    axs.plot(xs, ys, c="k", lw=width)
    axs.plot(xs, ys, c="r", lw=1)
    plt.gca().set_aspect('equal', adjustable='box')
    fig.suptitle("seed: " + str(seed))
    plt.show()

parser = argparse.ArgumentParser(description="Visualize a track previously stored in a file. If both -f and -s flags are present, only the -s one will be considered")

parser.add_argument("-f", "--file", help="Input file from where to load the track data.", default="", type=str)
parser.add_argument("-s", "--seed", help="Search the tracks/ directory for already generated tracks.", default="", type=str)
parser.add_argument("-w", "--width", type=int, help="Width of the track (default: 5)", default=5)

args = parser.parse_args()
if args.seed:
    try:
        file = "tracks/track_"+str(int(args.seed))+".npy"
    except ValueError:
        print("The input is not a valid seed.")
        exit()
    seed = args.seed
elif args.file:
    file = args.file
    seed = args.file.split("_")[1].split(".")[0]
else:
    print("At least one flag must be specified.")
    exit()
try:
    if not os.path.exists(file):
        raise IOError()
except IOError:
    print("The track with that seed doesn't exists, please generate that file using: python3 generate.py -q -s SEED -b 1")
    exit()

points = np.load(file)
plot(points,seed, args.width)
