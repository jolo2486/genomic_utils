# genomic_utils
Small but growing collection of utilities for various tasks related to computational genomics (nothing fancy).

# Scripts

## colorcmm
### '--help'
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

