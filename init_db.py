from sqlalchemy import create_engine, MetaData

from chat.settings import config
from chat.db import chat_user


DSN = "postgresql://{user}:{password}@{host}:{port}/{database}"


def setup_db():
    eng = create_engine(DSN.format(**config['postgres']))

    conf = config['postgres']
    db_name = conf['database']
    db_user = conf['user']
    db_pass = conf['password']

    conn = eng.connect()
    conn.execute("DROP DATABASE IF EXISTS %s" % db_name)
    conn.execute("DROP ROLE IF EXISTS %s" % db_user)
    conn.execute("CREATE USER %s WITH PASSWORD '%s'" % (db_user, db_pass))
    conn.execute("CREATE DATABASE %s ENCODING 'UTF8'" % db_name)
    conn.execute("GRANT ALL PRIVILEGES ON DATABASE %s TO %s" %
                 (db_name, db_user))
    conn.close()


def create_tables(eng):
    meta = MetaData()
    meta.create_all(bind=eng, tables=[chat_user])


def drop_tables(eng):
    meta = MetaData()
    meta.drop_all(bind=eng, tables=[chat_user])


if __name__ == '__main__':
    # setup_db()   # DROP DATABASE cannot run inside a transaction block error
    db_url = DSN.format(**config['postgres'])
    engine = create_engine(db_url)

    create_tables(engine)
