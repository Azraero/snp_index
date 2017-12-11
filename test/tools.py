from app.db import DB


def clean_db_cache(table):
    db = DB()
    db.execute("delete from {table};".format(table=table))

