import argparse
import sys
import random
import os

from datetime import datetime
from track import *

track_dir = "tracks/"
logs_dir = "logs/"

class colors:
    OKGREEN = "\033[92m"
    INFO = "\033[93m"
    FAIL = "\033[91m"
    CLOSE = "\033[0m"


def simple_log(data, filename="seeds.log"):
    with open(logs_dir + filename, 'a') as f:
        f.write(data)


description_str = "Procedural track generation using random Voronoi diagram."

parser = argparse.ArgumentParser(description=description_str, formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument("-v", "--verbose", help="Set verbosity level.", action="count", default=0)
parser.add_argument("--boundary", help="Specify the x and y values of the track boundary (default:  100 100).", nargs=2, type=int, default=[100, 100])
parser.add_argument("--npoints", type=int, help="The number of sites in the Voronoi diagram (points that generate the diagram) (default: 70).", default=70)
parser.add_argument("--softness", type=int, help="Percentage indicating the average smoothness of the corners (default: 66)", default=66)
parser.add_argument("--width", type=int, help="Width of the track (default: 5)", default=5)
parser.add_argument("--mode", choices=["bfs", "hull"], default="hull",
                    help="Track selection mode.\n" +
                    "\"bfs\" - using a bredth first-style visit for selection.\n" +
                    "\"hull\" - select the points inside a random convex hull (default).")
parser.add_argument("-s", "--seed", type=int, help="The seed used in generation.", default=random.randrange(sys.maxsize))
parser.add_argument("--cover", type=int, help="(bfs mode only) Percentage of the voronoi diagram area to be covered by the track selection (default: 50).", default=50)
parser.add_argument("--span", type=int, help="(hull mode only) Percentage of the boundary area in which the hull is generated (default: 50).", default=50)
parser.add_argument("-q", "--quiet", help="Disable plotting of the generated track.", default=False, action="store_true")
parser.add_argument("-b", "--batch", help="Number of tracks to generate and save.\n " +
                    "The generated tracks will be stored in " + track_dir +" in numpy array format (default: disabled). ", default=0, type=int)

args = parser.parse_args()
i = 0
if isinstance(args.seed, int):
    seed = args.seed

while i != args.batch or i == 0:
    # TODO: aggiungere controlli sul dominio dei vari args

    if len(args.boundary) == 2 and isinstance(args.npoints,int):
        track = Track(args.boundary, args.npoints, seed) #6928203095324602024
        if args.mode == "hull":
            perc = args.span/100.
        elif args.mode == "bfs":
            perc == args.cover/100.
        track.select(perc, method=args.mode)
        track.starting_line()
        min_radius = 0.3*args.softness/100.+0.1
        for c in track.corners:
            try:
                track.round(c, args.verbose, min_radius = min_radius)
            except ValueError:
                #temporary bad fix
                pass
        if not args.quiet:
            track.plot_track(width=args.width)
        if args.verbose:
            print(colors.INFO + "Generating track " + str(i + 1) + " with seed " + str(seed) + colors.CLOSE)
        try:
            os.mkdir(logs_dir)
        except:
            pass
        simple_log(datetime.now().strftime("[%d/%m/%Y %H:%M:%S]") + " " + str(seed) + "\n")
        if i < args.batch:
            try:
                os.mkdir(track_dir)
            except:
                pass
            track.store(track_dir + "track_" + str(seed) + ".npy")
            seed = random.randrange(sys.maxsize)
        else:
            break
        i = i + 1
    else:
        print("Wrong arguments.")
        break

    #boundary x e y
    #numero di punti
    #percentuale di voronoi selezionata
    #tondezza curve
    #larghezza del tracciato
