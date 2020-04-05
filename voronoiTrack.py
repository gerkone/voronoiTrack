import argparse
import sys
import random

from datetime import datetime
from track import *

description_str = "Procedural track generation using random Voronoi diagram."

parser = argparse.ArgumentParser(description=description_str, formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument("-v", "--verbose", help="Set verbosity level.", action="count", default=0)
parser.add_argument("--boundary", help="Specify the x and y values of the track boundary (default:  100 100).", nargs=2, type=int, default=[100, 100])
parser.add_argument("--npoints", type=int, help="The number of sites in the Voronoi diagram (points that generate the diagram) (default: 70).", default=70)
parser.add_argument("--softness", type=int, help="Percentage indicating the average smoothness of the corners (default: 66)", default=66)
parser.add_argument("--mode", choices=["bfs", "hull"], default="hull",
                    help="Track selection mode.\n" +
                    "\"bfs\" - using a bredth first-style visit for selection.\n" +
                    "\"hull\" - select the points inside a random convex hull (default).")
parser.add_argument("--seed", type=int, help="The seed used in generation.", default=random.randrange(sys.maxsize))
parser.add_argument("--cover", type=int, help="(bfs mode only) Percentage of the voronoi diagram area to be covered by the track selection (default: 50).", default=50)
parser.add_argument("--span", type=int, help="(hull mode only) Percentage of the boundary area in which the hull is generated (default: 50).", default=50)
# parser.add_argument("-q", "--quiet", help="Disable plotting of the generated track.", default=False, action="store_true")
# parser.add_argument("-b", "--batch", help="Number of tracks to generate and save.\n " +
#                     "The generated tracks will be stored in tracks/ (default: disabled). ", default=0, type=int)

# now = datetime.now()
# date_time = now.strftime("%Y%m%d%H%M%S")
# filename = "track_" + date_time + "_"+i+".trk"

args = parser.parse_args()

# TODO: aggiungere controlli sul dominio dei vari args

if len(args.boundary) == 2 and isinstance(args.npoints,int) and isinstance(args.seed,int):
    track = Track(args.boundary, args.npoints, args.seed)

if args.mode == "hull":
    perc = args.span/100.
elif args.mode == "bfs":
    perc == args.cover/100.
track.select(perc, method=args.mode)

# track.figure.plot()
track.starting_line()
track.flag_dense_corners()
min_radius = 0.3*args.softness/100.+0.1
for c in track.corners:
    track.round(c, min_radius = min_radius)
track.plot_track(width=16)

#boundary x e y
#numero di punti
#percentuale di voronoi selezionata
#tondezza curve
#larghezza del tracciato