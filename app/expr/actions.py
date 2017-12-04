from app.db import DB

def get_expr_table(table, gene_ids, groupA, groupB, map_groupA, map_groupB):
    db = DB()
    select_columns = ['GENE_ID', 'CHR', 'POS_START', 'POS_END'] + groupA + groupB
    select_columns_str = ','.join(select_columns)
    results = []
    for gene in gene_ids:
        cmd = "select {columns} from {table} where GENE_ID='{gene_id}';".format(
            columns=select_columns_str,
            table=table,
            gene_id=gene
        )
        result = db.execute(cmd, get_all=False)
        if not result:
            return (gene, '')
        results.append(list(result))
    return_select_columns =  ['GENE_ID', 'CHR', 'POS_START', 'POS_END'] + map_groupA + map_groupB
    return return_select_columns, results