import os

HOSTBNAME = 'localhost'
DATABASE = 'snp_index'
USERNAME = os.environ.get('USERNAME', 'onmaisiadmin')
PASSWORD = os.environ.get('PASSWORD', 'onmaisiadmin')
DB_URI = 'mysql://{}:{}@{}/{}'.format(
    USERNAME, PASSWORD, HOSTBNAME, DATABASE)
