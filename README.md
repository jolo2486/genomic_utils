# genomic_utils
Small but growing collection of utilities for various tasks related to computational genomics (nothing fancy).

# Scripts
These are standalone Python3 scripts with their own respective requirements and usage. Just download the scripts of interest and use --help or read below for more info.

*Tip:* In Linux: Remove the .py extention, make them executable with `chmod +x scriptname` and place them in `~/.local/bin/` or another place included in your PATH to use them as a regular command with e.g. `colorcmm --help` from anywhere in your system.

## colorcmm
```
Simple script to color the markers in a Chimera .cmm file according to a csv file of rgb values. The csv file should have
the format of three fields named "r,g,b" in that order and each record consist of the corresponding values, e.g. "0.1,
0.2, 0.3". The record index should directly correspond to the marker id that is to be colored.

optional arguments:
  -h, --help            show this help message and exit
  -in INFILE, --inFile INFILE
                        Path and name of the Chimera .cmm file to be updated
  -out [OUTFILE], --outFile [OUTFILE]
                        Path and name of the output file (optional).
  -rgb RGBFILE, --rgbFile RGBFILE
                        Path and name of a .csv file with only three fields named r,g,b and values where the row number
                        corresponds with the marker id.
```

### Usage
`./colorcmm.py -in <path> -out <path> -rgb <path>` will produce a new .cmm file with the markers updated with the new rgb values specified in the rgb file.

`./colorcmm.py -in <path> -rgb <path>` will print the contents of the updated cmm file to std.out.

## ABcompart
```
usage: ABcompartmentalize [-h] -clr CLRFILE -bz BINSIZE [-chr CHROMS] -refg REFGENOMEFILE [-neigs NEIGS]
                          [-eig EIGENVECTOR] [-out OUTFILE]

This script uses Cooltools and Bioframe to perform eigendecomposition on the Hi-C matrix of a specific resolution
(binsize) from a multiresolution .mcool file. Returns a csv list of A, B compartments according to the specified
eigenvector. It will align the eigenvector using GC content as a phasing track. For this a reference genome fasta file
such as hg38.fa is required. This can be obtained by e.g.

wget -P https://hgdownload.cse.ucsc.edu/goldenpath/hg38/bigZips/hg38.fa.gz

If -chr is not specified, it will default to "chr1, chr2, ...,chr22, chrX, chrY".

optional arguments:
  -h, --help            show this help message and exit
  -clr CLRFILE, --clrFile CLRFILE
                        Path to the cooler multiresolution .mcool file
  -bz BINSIZE, --binsize BINSIZE
                        Resolution to use. (Must be available in the .mcool file.)
  -chr CHROMS, --chroms CHROMS
                        Comma separated list of available chromosome names, e.g. "chr1, chr2, ..., chrY" (optional)
  -refg REFGENOMEFILE, --refGenomeFile REFGENOMEFILE
                        Path to the reference genome fasta file, e.g. hg38.fa
  -neigs NEIGS, --neigs NEIGS
                        Number of eigenvectors to compute.
  -eig EIGENVECTOR, --eigenvector EIGENVECTOR
                        Which eigenvector to use for compartmentalization.
  -out OUTFILE, --outFile OUTFILE
                        Path to a csv file to store A, B compartmentalization. (optional)
```
### Usage
`./ABcompart.py -clr coolfile.mcool -bz 160000 -refg 'hg38.fa' -neigs 2 -eig 1 -out abcompartments.csv` will produce a .csv file with two fields named 'A' and 'B', and records consisting of pairs of bin id:s.

`./ABcompart.py -clr coolfile.mcool -bz 160000 -refg 'hg38.fa' -neigs 2 -eig 1` will print the contents described above to std.out.

### Requirements
- pandas: `pip install pandas`
- cooler: `pip install cooler`
- cooltools: `pip install cooltools`
- bioframe: `pip install bioframe`

## colorgroups
```
usage: colorcmm [-h] -g GROUPDATA -c COLORS [-out OUTFILE]

A little helper script to color groups. Creates (or prints to std.out) a csv
file of rgb values given a csv file with fields of group names A,B,C,... and
records of bin ids, as well as a csv file of group colors with fields of the
same group names A,B,C,... but three records red, green, blue with
corresponding values for each group. The output file will have as many records
as the maximum index found in the groups file. If any indices are left out of
the groups, they will be colored white (1,1,1). The indices in the out file
will hence correspond to bin ids.

optional arguments:
  -h, --help            show this help message and exit
  -g GROUPDATA, --groupData GROUPDATA
                        Path to a csv file with the groups.
  -c COLORS, --colors COLORS
                        Path to the csv color file.
  -out OUTFILE, --outFile OUTFILE
                        Path to the output rgb csv file (optional).
```
### Usage
`./colorgroups.py -g example_groups.csv -c example_colors.csv -out example_rgbout.csv` will produce a .csv file example_rgbout.csv with fields 'r,g,b', and records consisting values e.g. '0.1,0.2,0.3'.

`./colorgroups.py -g testgroups.csv -c testcolors.csv -out testout.csv` will print the contents described above to std.out.

Please refer to the example files for the proper file formatting.

### Requirements
- pandas: `pip install pandas`
- numpy: `pip install numpy`

## colortrack
```
usage: colortrack [-h] [-in INFILE] [-out [OUTFILE]] -cmap CMAP

Helper function to take a list of floats and a matplotlib cmap and create or
print a csv file of rgb-values. This can then be used in conjunction with
colorcmm to color a Chimera file according to a track such as GC-percentage or
GPSeq score. The list should either be provided as comma separated
'1,2,3,4,...' or just as one value per line.

optional arguments:
  -h, --help            show this help message and exit
  -in INFILE, --inFile INFILE
                        Path to the csv format track to color by, e.g. GC or
                        GPSeq score track. Exclude to read from stdin.
  -out [OUTFILE], --outFile [OUTFILE]
                        Path to the output file (optional). Exclude to write
                        to stdout
  -cmap CMAP, --cmap CMAP
                        Name of the matplotlib color map.
```
### Example Usage
`./colortrack.py -in example_track.csv -cmap 'autumn' -out outfile.csv` will produce a .csv file outfile.csv with fields 'r,g,b', and records consisting rgb values e.g. '0.1,0.2,0.3' according to
the [matplotlib colormap](https://matplotlib.org/stable/gallery/color/colormap_reference.html) 'autumn'.

`./colortrack.py -in example_track.csv -cmap 'autumn'` will print the contents described above to std.out.

`echo '1,2,3,4,5' | ./colortrack.py -cmap 'autumn'` would output:

```
r,g,b
1.0,0.0,0.0
1.0,0.2,0.0
1.0,0.4,0.0
1.0,0.6,0.0
1.0,0.8,0.0
1.0,1.0,0.0
1.0,1.0,0.0
```

```
### Requirements
- matplotlib: `pip install matplotlib`
- numpy: `pip install numpy`
