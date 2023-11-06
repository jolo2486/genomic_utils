#!/usr/bin/env python3
import argparse, os
import numpy as np
import pandas as pd

def file_path(string):
    if os.path.exists(string):
        return string
    else:
        raise NotADirectoryError(string)

parser = argparse.ArgumentParser(
    prog='chromlink_cmm',
    description="""
                Link chromosomes together in CMM files.
                """
)
# arguments
parser.add_argument(
    '-in',
    '--inFile',
    type=file_path,
    help='Path to the Chimera .cmm file to be updated',
    required= True
)
parser.add_argument(
    '-out',
    '--outFile',
    type=str,
    help='Path to the output cmm file (optional).',
    nargs='?', # the nr of times the arg can be used (? makes it optional)
    default=None,
    required=True
)
parser.add_argument(
    '-rgb',
    '--rgbFile',
    type=file_path,
    help="""
        Path and name of a .csv file with only three fields named r,g,b and
        values where the row number corresponds to the chromosome number; no headers.
        """,
    required=False
)
parser.add_argument(
    '-L',
    '--lFile',
    type=file_path,
    help='Path to the L-file with chromosome label per bin, i.e. L=[1,1,1,...,24]',
    required= True
)
args = parser.parse_args()

L_vec = np.fromfile(args.lFile, dtype='uint8')
chromosomes = sorted(list(set(L_vec)))
# Default colors as used in Chromflock:
chromosome_colors = {
    1: (240, 163, 255),
    2: (0, 117, 220),
    3: (153, 63, 0),
    4: (76, 0, 92),
    5: (25, 25, 25),
    6: (0, 92, 49),
    7: (43, 206, 72),
    8: (255, 204, 153),
    9: (128, 128, 128),
    10: (148, 255, 181),
    11: (143, 124, 0),
    12: (157, 204, 0),
    13: (194, 0, 136),
    14: (0, 51, 128),
    15: (255, 164, 5),
    16: (255, 168, 187),
    17: (66, 102, 0),
    18: (255, 0, 16),
    19: (94, 241, 242),
    20: (0, 153, 143),
    21: (224, 255, 102),
    22: (116, 10, 255),
    23: (153, 0, 0),
    24: (255, 255, 128)
}
if args.rgbFile:
    ccols = pd.read_csv(args.rgbFile, sep=',', header=None).values
    chromosome_colors = {i + 1: ccols[i] for i, v in enumerate(ccols)}
chrom_colors = {
    c: np.round(np.array(chromosome_colors[c]) / 255, 4) for c in chromosome_colors
}
# Processing links and markers
cmm_links = []; cmm_markers = []
for c in chromosomes:
    chrom_bins = [i for i, v in enumerate(L_vec) if v == c]
    rgb = chrom_colors[c]
    for i in range(len(chrom_bins) - 1):
        cmm_links.append(f'<link id1="{chrom_bins[i]}" id2="{chrom_bins[i+1]}" r="{rgb[0]}" g="{rgb[1]}" b="{rgb[2]}" radius="0.006251"/>\n')
with open(args.inFile, 'r') as infile:
    for line in infile:
        if line.startswith("<marker_set") or line.startswith("<marker id"):
            cmm_markers.append(line)
with open(args.outFile, 'w') as outfile:
    for line in cmm_markers + cmm_links:
        outfile.write(line)
    outfile.write("</marker_set>")
