# coding:utf-8
import os
import sys
import click
import pandas as pd
# from datetime import datetime

# default to snp_index/data/
base_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))

@click.command()
@click.option('--locusfile', help='a gene locus file')
@click.option('--annfile', help='a gene ann file')
@click.option('--outfile', help='output file name', default='gene_mlocus')
@click.option('--sep', help='sep file string', default='\t')
def merge_table(locusfile, annfile, outfile, sep):
    try:
        locus_table = pd.read_table(locusfile, sep=sep,
                                    names=['Gene_ID', 'Chr', 'Start', 'End', 'Direct'])
        ann_table = pd.read_table(annfile, sep=sep,
                                  names=['Gene-ID', 'Blast_Hit', 'Description'])
    except IOError as e:
        print e
        sys.exit(1)
    mergeTab = pd.merge(locus_table, ann_table,
                        left_on='Gene_ID', right_on='Gene-ID',
                        how='left')
    mergeTab = mergeTab.drop('Gene-ID', axis=1)
    Output = os.path.join(base_dir, 'data', outfile)
    mergeTab.to_csv(Output, index=False, sep='\t', na_rep='Na')


if __name__ == '__main__':
    merge_table()




