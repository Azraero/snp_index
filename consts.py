import os

HOSTBNAME = 'localhost'
DATABASE = 'snp_index'
USERNAME = os.environ.get('USERNAME', 'root')
PASSWORD = os.environ.get('PASSWORD', '050400')
DB_URI = 'mysql://{}:{}@{}/{}'.format(
    USERNAME, PASSWORD, HOSTBNAME, DATABASE)
