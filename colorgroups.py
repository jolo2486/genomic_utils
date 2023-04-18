#!/usr/bin/env python3
import argparse, os
import pandas as pd
import numpy as np

def file_path(string):
    if os.path.exists(string):
        return string
    else:
        raise NotADirectoryError(string)
parser = argparse.ArgumentParser(
    prog='colorcmm',
    description="""
                A little helper script to color groups.
                Creates (or prints to std.out) a csv file of rgb values
                given a csv file with fields of group names A,B,C,...
                and records of bin ids, as well as a csv file of group
                colors with fields of the same group names A,B,C,...
                but three records red, green, blue with corresponding values
                for each group. The output file will have as many records as
                the maximum index found in the groups file. If any indices
                are left out of the groups, they will be colored white (1,1,1).

                The indices in the out file will hence correspond to bin ids.
                """
)
# arguments
parser.add_argument(
    '-g',
    '--groupData',
    type=file_path,
    help='Path to a csv file with the groups.',
    required= True
)
parser.add_argument(
    '-c',
    '--colors',
    type=file_path,
    help='Path to the csv color file.',
    required=True
)
parser.add_argument(
    '-out',
    '--outFile',
    type=str,
    help='Path to the output rgb csv file (optional).',
    required=False
)
args = parser.parse_args()
groups = pd.read_csv(args.groupData)
colors = pd.read_csv(args.colors)
maxid = max([e for group in groups for e in groups[group]])
# Initialize everything to white, i.e 1,1,1
rgbvals = np.ones((maxid+1,3))
for g in groups:
    for idx in groups[g]:
        rgbvals[idx] = np.array(colors[g])
if args.outFile:
    with open(args.outFile, 'w') as f:
        f.write('r,g,b\n')
        for line in rgbvals:
            f.write(f'{line[0]},{line[1]},{line[2]}\n')
else:
    print('r,g,b')
    for line in rgbvals:
        print(f'{line[0]},{line[1]},{line[2]}')
