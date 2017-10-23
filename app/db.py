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
