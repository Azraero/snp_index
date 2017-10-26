import os

HOSTBNAME = 'localhost'
DATABASE = 'snp_index'
USERNAME = os.environ.get('USERNAME', 'root')
PASSWORD = os.environ.get('PASSWORD', '050400')
DB_URI = 'mysql://{}:{}@{}/{}'.format(
    USERNAME, PASSWORD, HOSTBNAME, DATABASE)

get_head_cmd = """
    select column_name from information_schema.columns
    where table_schema='snp_index' and table_name='{}';
    """
get_unique_cmd = "select distinct() from {};"

create_expr_cmd = """
                  create table {}(Id INT PRIMARY KEY AUTO_INCREMENT,
                                  GENE_ID VARCHAR(20),
                                  CHR VARCHAR(5),
                                  POS_START VARCHAR(50),
                                  POS_END VARCHAR(50),
                  """


create_snp_cmd = """
                   create table {}(Id INT PRIMARY KEY AUTO_INCREMENT,
                                   CHR VARCHAR(5),
                                   POS VARCHAR(50),
                                   REF VARCHAR(10),
                                   ALT VARCHAR(10),
                                   FEATURE VARCHAR(50),
                                   GENE VARCHAR(100),
                   """

create_group_cmd = """
                   create table {}(Id INT PRIMARY KEY AUTO_INCREMENT,
                                   SAMPLE VARCHAR(20),
                                   DESCRIPTION VARCHAR(100),
                   """

snp_table_info = {'cmd': create_snp_cmd,
                  'fixed_column_num': 6,
                  'fixed_column_name': ('CHR', 'POS', 'REF', 'ALT', 'FEATURE', 'GENE'),
                  'add_key_str': ',key chrindex (CHR), key posindex (POS)'}

expr_table_info = {'cmd': create_expr_cmd,
                   'fixed_column_num': 4,
                   'fixed_column_name': ('GENE_ID', 'CHR', 'POS_START', 'POS_END'),
                   'add_key_str': ',key geneindex (GENE_ID)'}
                   
relative_table = {'snp_mRNA_table': 'expr_gene_pos'}
table_info = {'snp': snp_table_info,
              'expr': expr_table_info}
