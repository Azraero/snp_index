import os
from app.db import DB
from settings import basedir
import subprocess

BASE_DB_DIR = "/var/www/html/viroblast/db"
BLAST_CDS_DB = "nucleotide/triticum_aestivum.transcript"
BLAST_PROTEIN_DB = "protein/triticum_aestivum.trans.pro"
BLAST_OUT_PATH = os.path.join(basedir, 'app', 'static', 'blast_results')


def run_blast_result(genename):
    # before run blast rm last search results anyway
    if os.listdir(BLAST_OUT_PATH):
        rm_cmd = 'rm {}'.format(os.path.join(BLAST_OUT_PATH, '*'))
        subprocess.call(rm_cmd, shell=True)

    # get search trans genes
    db = DB()
    results = db.execute("select GENE_TRANS from geneTrans_map where GENE='{gene}'".format(gene=genename))
    results = [result[0] for result in results]
    if results:
        blast_cmd = "blastdbcmd -entry {genename} -db '{db}' -line_length 100 -out {out}"
        for gene_trans in results:
            run_cds_cmd = blast_cmd.format(genename=gene_trans,
                                           db=os.path.join(BASE_DB_DIR, BLAST_CDS_DB),
                                           out=os.path.join(BLAST_OUT_PATH,  'gene.cds.' + gene_trans))
            run_protein_cmd = blast_cmd.format(genename=gene_trans,
                                               db=os.path.join(BASE_DB_DIR, BLAST_PROTEIN_DB),
                                               out=os.path.join(BLAST_OUT_PATH, 'gene.protein.' + gene_trans))
            subprocess.call(run_cds_cmd, shell=True)
            subprocess.call(run_protein_cmd, shell=True)
        blast_results = get_blast_result(results)
        return blast_results
    return {}


def get_blast_result(trans_results):
    blast_seq_dict = {}
    cds_seq_list = []
    pro_seq_list = []
    try:
        for each in trans_results:
            with open(os.path.join(BLAST_OUT_PATH, 'gene.cds.' + each), 'r+') as cds_info:
                cds_list = cds_info.readlines()
                cds_seq = ''.join([row for row in cds_list[1:]])
                cds_seq_list.append(cds_seq)
            with open(os.path.join(BLAST_OUT_PATH, 'gene.protein.' + each), 'r+') as pro_info:
                pro_list = pro_info.readlines()
                pro_seq = ''.join([row for row in pro_list[1:]])
                pro_seq_list.append(pro_seq)
    except IOError:
        print 'not find files'
        return blast_seq_dict
    blast_seq_dict['cds_seq'] = dict(zip(trans_results, cds_seq_list))
    blast_seq_dict['pro_seq'] = dict(zip(trans_results, pro_seq_list))
    return blast_seq_dict


def get_locus_result(genename, blast_results):
    cds_seq_dict = blast_results.get('cds_seq', 'NA')
    pro_seq_dict = blast_results.get('pro_seq', 'NA')
    db = DB()
    locus_result = {}
    cmd = """select l.*, f.BLAST_Hit_Accession, f.Description, f.Pfam_ID,
             f.Interpro_ID, f.GO_ID from locus l left join func f
             on l.GENE_ID=f.GENE_ID where l.GENE_ID='{0}';
          """.format(genename)
    result = db.execute(cmd, get_all=False)
    if result:
        gene_id, chr, pos_start, pos_end = result[1:5]
        blast_hit, description, pfam_id, interpro_id, go_id = result[5:]
        locus_result['gene_identification'] = {'Gene Product Name': description,
                                               'Locus Name': genename}
        locus_result['gene_attributes'] = {'Chromosome': chr,
                                           "Gene Postion":'{start} - {end}'.format(start=pos_start, end=pos_end)}
        header = ['Accession', 'Description', 'Pfam_ID', 'Interpro_ID', 'GO_ID']
        locus_result['gene_annotation'] = {}
        locus_result['gene_annotation']['header'] = header
        locus_result['gene_annotation']['body'] = [blast_hit, description, pfam_id, interpro_id, go_id]
        locus_result['gene_cds_seq'] = cds_seq_dict
        locus_result['gene_pro_seq'] = pro_seq_dict
    return locus_result
