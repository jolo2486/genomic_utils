#!/usr/bin/env python3
import argparse
import os
import cooler
import cooltools
import bioframe
import pandas as pd
import warnings

def file_path(string):
    if os.path.exists(string):
        return string
    else:
        raise NotADirectoryError(string)

parser = argparse.ArgumentParser(
    prog='ABcompartmentalize',
    description="""
                This script uses Cooltools and Bioframe to perform eigendecomposition on
                the Hi-C matrix of a specific resolution (binsize) from a multiresolution
                .mcool file. Returns a csv list of A, B compartments according to the
                specified eigenvector. It will align the eigenvector using GC content as
                a phasing track. For this a reference genome fasta file such as hg38.fa
                is required. This can be obtained by e.g.

                wget -P ./data/ https://hgdownload.cse.ucsc.edu/goldenpath/hg38/bigZips/hg38.fa.gz

                If -chr is not specified, it will default to "chr1, chr2, ..., chrX, chrY".
                """
)
# arguments
parser.add_argument(
    '-clr',
    '--clrFile',
    type=file_path,
    help='Path to the cooler multiresolution .mcool file',
    required= True
)
parser.add_argument(
    '-bz',
    '--binsize',
    type=int,
    help='Resolution to use. (Must be available in the .mcool file.)',
    required=True
)
parser.add_argument(
    '-chr',
    '--chroms',
    type=str,
    help='Comma separated list of available chromosome names, e.g. "chr1, chr2, ..., chrY" (optional)',
    required=False
)
parser.add_argument(
    '-refg',
    '--refGenomeFile',
    type=file_path,
    help='Path to the reference genome fasta file, e.g. hg38.fa',
    default=None,
    required=True
)
parser.add_argument(
    '-neigs',
    '--neigs',
    type=int,
    help="""
        Number of eigenvectors to compute.
        """,
    default=2,
    required=False
)
parser.add_argument(
    '-eig',
    '--eigenvector',
    type=int,
    help="""
        Which eigenvector to use for compartmentalization.
        """,
    default=1,
    required=False
)
parser.add_argument(
    '-out',
    '--outFile',
    type=str,
    help='Path to a csv file to store A, B compartmentalization. (optional)',
    required= False
)
args = parser.parse_args()
if args.chroms:
    chromnames = [s.strip() for s in args.chroms.split(',')]
else:
    chromnames = [f'chr{i}' for i in range(1, 23)] + ['chrX', 'chrY']
print(f'Loading and filtering bins for {args.clrFile}...')
clr = cooler.Cooler(f'{args.clrFile}::resolutions/{str(args.binsize)}', mode='r')
# only use records that is in chromnames
bins = clr.bins()[:][clr.bins()['chrom'][:].isin(chromnames)]

# Remove unused categories from all categorical columns
# This caused trouble when binning the gc content below
for col in bins.select_dtypes(include='category'):
    bins[col] = bins[col].cat.remove_unused_categories()
chromsizes = []
for i in chromnames:
    chromsizes.append(clr.chromsizes[i])
view_df = pd.DataFrame(
    {'chrom': chromnames,
     'start': 0,
     'end': chromsizes,
     'name': chromnames}
)
# Ignore the pandas FutureWarning caused by bioframes groupby operation
warnings.simplefilter(action='ignore', category=FutureWarning)
# retrieve GC track from hg38
print(f'Loading GC track from {args.refGenomeFile}...')
hg38_genome = bioframe.load_fasta(args.refGenomeFile)
gc_cov = bioframe.frac_gc(bins[['chrom', 'start', 'end']], hg38_genome)
print('Computing eigenvectors...')
cis_eigs = cooltools.eigs_cis(
    clr,
    gc_cov,
    view_df=view_df,
    n_eigs=args.neigs,
)
try:
    eigv = 'E'+str(args.eigenvector)
    pc = cis_eigs[1][eigv]
except KeyError as ke:
    print(f'Eigenvector {args.eigenvector} is not computed!', ke)
else:
    # nan < 0, nan > 0 both return False, hence the following should pick out all numbers.
    A_comp = [i for i, v in enumerate(pc) if v > 0]
    B_comp = [i for i, v in enumerate(pc) if v < 0]
    fields = ['A,B']
    records = [f'{a},{b}' for a, b in zip(A_comp, B_comp)]
    print(f'Summary: Total bins: {len(clr.bins())}, length A: {len(A_comp)}, length B: {len(B_comp)}')
    if args.outFile:
        with open(args.outFile, 'w') as f:
            for line in fields + records:
                f.write(f'{line}\n')
    else:
        for line in fields + records:
            print(line)
