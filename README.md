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