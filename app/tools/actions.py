from app.db import DB

def get_locus_result(genename):
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
                                           "CDS Coordinates (5'-3')":'{0} - {1}'.format(pos_start,
                                                                                        pos_end)}
        header = ['Accession', 'Description', 'Pfam_ID', 'Interpro_ID', 'GO_ID']
        locus_result['gene_annotation'] = {}
        locus_result['gene_annotation']['header'] = header
        locus_result['gene_annotation']['body'] = [blast_hit, description, pfam_id, interpro_id, go_id]
    return locus_result