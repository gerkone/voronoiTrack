import argparse
import matplotlib.pyplot as plt
import numpy as np

def read_points(data):
    xs = []
    ys = []
    for q in data:
        xs.append(q[0])
        ys.append(q[1])
    return xs, ys

def plot(data, seed):
    xs, ys = read_points(data)

    fig, axs = plt.subplots(1, 1, constrained_layout=True)
    axs.plot(xs, ys, c="k", lw=5)
    axs.plot(xs, ys, c="r", lw=1)
    fig.suptitle("seed: " + str(seed))
    plt.show()

parser = argparse.ArgumentParser(description="Visualize a track previously stored in a file.")

parser.add_argument("file", help="Input file from where to load the track data.", default="", type=str)

args = parser.parse_args()
#ugly
seed = args.file.split("_")[1].split(".")[0]

points = np.load(args.file)
plot(points,seed)


