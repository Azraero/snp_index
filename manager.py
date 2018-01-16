# coding=utf-8
from flask_script import Manager, Server
from flask_migrate import MigrateCommand
from app.auth.models import User, Snptable
from app.exetensions import db
from app.app import create_app

app = create_app('prod')
manager = Manager(app)
manager.add_command('runserver',
                    Server(host='0.0.0.0',
                           port=9000))

manager.add_command('db', MigrateCommand)


@manager.command
def test():
    """run the unit tests"""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


@manager.command
def init_db():
    db.create_all()
    chencheng = User(username='chencheng',
                     email='291552579@qq.com',
                     password='050400',
                     actvie=True,
                     is_admin=True)
    db.session.add(chencheng)
    db.session.commit()

    tables = [Snptable(tablename='snp_mRNA_snp_ann_table',
                       tabletype='snp',
                       owner='chencheng'),
              Snptable(tablename='expr_gene_tmp_pos',
                       tabletype='expr',
                       owner='chencheng')]
    db.session.add_all(tables)
    db.session.commit()


if __name__ == '__main__':
    manager.run()
