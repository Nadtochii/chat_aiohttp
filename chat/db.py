import aiopg.sa
import sqlalchemy as sa

from chat.settings import config


meta = sa.MetaData()

chat_user = sa.Table(
    'chat_user', meta,
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('username', sa.String(64), nullable=False),
    sa.Column('password', sa.String(200), nullable=False)
)


async def init_pg(app):
    conf = config['postgres']
    engine = await aiopg.sa.create_engine(
        database=conf['database'],
        user=conf['user'],
        password=conf['password'],
        host=conf['host'],
        port=conf['port'],
        minsize=conf['minsize'],
        maxsize=conf['maxsize'])
    app['db'] = engine


async def close_pg(app):
    app['db'].close()
    await app['db'].wait_closed()
