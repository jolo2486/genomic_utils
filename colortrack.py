#!/usr/bin/env python3
import argparse, os
import csv
import numpy as np
import matplotlib.colors as mcolors
from matplotlib import pyplot as plt

def file_path(string):
    if os.path.exists(string):
        return string
    else:
        raise NotADirectoryError(string)

parser = argparse.ArgumentParser(
    prog='colortrack',
    description="""
                Helper function to take a list of floats and a matplotlib cmap and create or print a
                csv file of rgb-values. This can then be used in conjunction with colorcmm to color
                a Chimera file according to a track such as GC-percentage or GPSeq score. The list
                should either be provided as comma separated '1,2,3,4,...' or just as one value per
                line.
                """
)
parser.add_argument(
    '-in',
    '--inFile',
    type=file_path,
    help='Path to the csv format track to color by, e.g. GC or GPSeq score track. Leave out to read from stdin.',
    required=False
)
parser.add_argument(
    '-out',
    '--outFile',
    type=str,
    help='Path to the output file (optional). Exclude to write to stdout',
    nargs='?', # the nr of times the arg can be used (? makes it optional)
    default=None,
    required=False
)
parser.add_argument(
    '-cmap',
    '--cmap',
    type=str,
    help="""
        Name of the matplotlib color map.
        """,
    required=True
)
args = parser.parse_args()

def vec2rgb(vec, cmap):
    """Takes a vector, and a maplotlib cmap name and returns np.ndarray of rgb triplets."""
    norm = mcolors.Normalize(vmin=min(vec), vmax=max(vec))
    normalized_values = norm(vec)
    cmap = plt.get_cmap(cmap)
    rgb_colors = np.array([cmap(value)[:3] for value in normalized_values])
    return rgb_colors

if args.inFile:
    track_vec = np.loadtxt(args.inFile, delimiter=',', dtype=float)
else:
    stdin = os.sys.stdin.read().rstrip()
    track_vec = stdin.replace(' ', '').replace('\n', ',').split(',')
    try:
        track_vec = np.array([float(char) for char in track_vec])
    except ValueError as ve:
        print("Input string was not a well formatted list of values!")

if args.outFile:
    with open(args.outFile, 'w') as f:
        f.write('r,g,b\n')
        for line in vec2rgb(track_vec, args.cmap):
            f.write(f'{line[0]},{line[1]},{line[2]}\n')
else:
    print('r,g,b')
    for line in vec2rgb(track_vec, args.cmap):
        print(f'{line[0]},{line[1]},{line[2]}')