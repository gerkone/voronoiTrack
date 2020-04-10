# voronoiTrack
Procedural 2D track generation using randomly generated Voronoi diagram.

**This project is still in early developement, many solutions are temporary and many options are not available.**

## Requirements
- \>=Python 3.7
- Numpy
- Scipy
- Matplotlib

## Usage
The script that is used to generate the track is `generate.py`. Some options regarding the building of the diagram and the track are available:
- `--boundary MAXX MAXY`, the space in which work;
- `--npoints N`, the number of starting points (*usually* affects the track complexity);
- `--softness P`, a indicative number for the "smoothness" of the corners.
Some options regarding the track selection mode:
- `--cover PERC`, used for the "bfs" selection mode. Sets the upper bound of the area to be covered as percentage of the total area (area of every cell);
- `--span PERC`, used in the "hull" mode. Sets the boundary in which to generate the hull points as percentage of the `boundary`.

The tracks generated using the `generate.py` script can be stored as 2 dimensional point array (in numpy format) by specifying the batch size with `-b SIZE`/`--batch SIZE`.
Saved tracks can be later visualized using the `visualize.py` script.

## How does it work
The method used can be defided in 3 steps:
- **Initialization**: Create the Voronoi diagram and initialize the data structures.
- **Track seletion**: Mark the set of cells (Voronoi enclosed regions) that will "build" the track.
- **Rounding**: Round/soften the "corners".
### Initialization
Input variables: n: number of points, boundary: accepted space.

A Voronoi diagram is produced starting from a set of n random points. Infinite/imaginary and out-of-bounds vertices are excluded.
### Track selection
Two different ways of selecting cells are present:
#### BFS: 
Input variables: cover: percentage of the total area to be covered.

The Voronoi diagram can be seen as an wheighted undirected graph, where the cells are nodes with area as weight and shared edges as connections. Starting from a random node, we explore the graph marking every new node, until we reach the "cover" percentage of area.
#### Hull:
Input variables: span: percentage of the boundary where the hull is generated.

A more geometric view is to take a random convex hull (inside the "span" boundary) and mark as selected all the cells that have at least one vertex inside the hull.
