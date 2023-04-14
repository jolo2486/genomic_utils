#!/usr/bin/env python3
import argparse, os
import warnings
import csv
import re
from xml.etree import ElementTree as ET

def file_path(string):
    if os.path.exists(string):
        return string
    else:
        raise NotADirectoryError(string)
def replace_rgb_values(marker_string, rgb_values):
    """Returns a replacement string for a line in .cmm file with updated rgb values
    args:
    marker_string -- (string) marker-line of .cmm file, starting with '<marker id='
    rgb_values -- (dict) the new rgb values for the marker, e.g. {'r':1,'g':2,'b':3}
    """
    def replace_value(match):
        attribute=match.group(1)
        value=rgb_values[attribute]
        return f'{attribute}="{value:.6f}"'
    updated_marker_string=re.sub(
        r'(r|g|b)=("[^"]*")', replace_value, marker_string)
    return updated_marker_string
parser = argparse.ArgumentParser(
    prog='colorcmm',
    description="""
                Simple script to color the markers in a Chimera .cmm file according
                to a csv file of rgb values. The csv file should have the format of
                three fields named "r,g,b" in that order and each record consist of
                the corresponding values, e.g. "0.1, 0.2, 0.3". The record index
                should directly correspond to the marker id that is to be colored.
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
    help='Path to the output file (optional).',
    nargs='?', # the nr of times the arg can be used (? makes it optional)
    default=None,
    required=False
)
parser.add_argument(
    '-rgb',
    '--rgbFile',
    type=file_path,
    help="""
        Path and name of a .csv file with only three fields named r,g,b and
        values where the row number corresponds with the marker id.
        """,
    required=True
)
args = parser.parse_args()

# read the csv rgbFile and convert it to a dict
with open(args.rgbFile, 'r') as rgbf:
    reader = csv.DictReader(rgbf)
    rgb_values = [{k: int(v) for k, v in row.items()} for row in reader]
# check wether .cmm file is XML
with open(args.inFile, 'r') as f:
    try:
        cmm_lines=f.readlines()
        ET.fromstring(''.join(cmm_lines))
    except ParseError as e:
        raise Exception('Not a well formatted XML file!') from e
# create updated markers with colors from rgbFile
new_markers={}
for i, line in enumerate(cmm_lines):
    if line.startswith('<marker id='):
        index=int(re.search(r'<marker id="([^"]+)"', line).group(1))
        rgb=rgb_values[index]
        new_markers[index]=replace_rgb_values(line, rgb)
if not new_markers:
    warnings.warn('No new markers created! Did the .cmm contain any markers?')
for i, line in enumerate(cmm_lines):
    if line.startswith('<marker id='):
        marker_id=int(re.search(r'<marker id="([^"]+)"', line).group(1))
        rgb=rgb_values[marker_id]
        new_markers[marker_id]=(i, replace_rgb_values(line, rgb))
# update the lines from .cmm file with the new markers
for marker_id in new_markers:
    cmm_lines[new_markers[marker_id][0]]=new_markers[marker_id][1]
# write the updated lines to a new .cmm file
if args.outFile:
    with open(args.outFile, 'w') as f:
        for line in cmm_lines:
            f.write(line)
else:
    for line in cmm_lines:
        print(line, end='')

