import os
from app.db import DB
from settings import basedir
import subprocess

BASE_DB_DIR = "/var/www/html/viroblast/db"
BLAST_CDS_DB = "nucleotide/triticum_aestivum.transcript"
BLAST_PROTEIN_DB = "protein/triticum_aestivum.trans.pro"
BLAST_OUT_PATH = os.path.join(basedir, 'app', 'static', 'blast_results')


def run_blast_result(genename):
    # rm last search results
    rm_cmd = 'rm {}'.format(os.path.join(BLAST_OUT_PATH, '*'))
    subprocess.call(rm_cmd, shell=True)

    blast_cmd = "blastdbcmd -entry {genename} -db '{db}' -out {out}"
    run_cds_cmd = blast_cmd.format(genename=genename,
                                   db=os.path.join(BASE_DB_DIR, BLAST_CDS_DB),
                                   out=os.path.join(BLAST_OUT_PATH,  'gene.cds'))
    run_protein_cmd = blast_cmd.format(genename=genename,
                                       db=os.path.join(BASE_DB_DIR, BLAST_PROTEIN_DB),
                                       out=os.path.join(BLAST_OUT_PATH, 'gene.protein'))
    subprocess.call(run_cds_cmd, shell=True)
    subprocess.call(run_protein_cmd, shell=True)
    blast_results = get_blast_result()
    return blast_results


def get_blast_result():
    blast_seq_dict = {}
    try:
        with open('gene.cds', 'r+') as cds_info:
            cds_list = cds_info.readlines()
            cds_seq = ''.join([row.strip() for row in cds_list[1:]])
            cds_cds = cds_list[0].strip().split(' ')[-1].split('=')[1]
            blast_seq_dict['cds_seq'] = cds_seq
            blast_seq_dict['cds_pos'] = cds_cds
        with open('gene_protein', 'r+') as pro_info:
            pro_list = pro_info.readlines()
            pro_seq = pro_list[-1].strip()
            blast_seq_dict['pro_seq'] = pro_seq
    except IOError:
        return blast_seq_dict
    return blast_seq_dict


def get_locus_result(genename, blast_results):
    cds = blast_results.get('cds_pos', 'NA')
    cds_seq = blast_results.get('cds_seq', 'NA')
    pro_seq = blast_results.get('pro_pos', 'NA')
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
                                           "CDS Coordinates (5'-3')":'{}'.format(cds)}
        header = ['Accession', 'Description', 'Pfam_ID', 'Interpro_ID', 'GO_ID']
        locus_result['gene_annotation'] = {}
        locus_result['gene_annotation']['header'] = header
        locus_result['gene_annotation']['body'] = [blast_hit, description, pfam_id, interpro_id, go_id]
        locus_result['gene_cds_seq'] = cds_seq
        locus_result['gene_pro_seq'] = pro_seq
    return locus_result
