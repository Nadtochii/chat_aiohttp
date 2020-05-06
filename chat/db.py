import aiopg.sa
import sqlalchemy as sa

from chat.settings import config


meta = sa.MetaData()

chat_user = sa.Table(
    'chat_user', meta,
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('username', sa.String(64), nullable=False),
    sa.Column('password', sa.String(200), nullable=False),

    sa.PrimaryKeyConstraint('id', name='chat_user_id_pkey')
)

chat = sa.Table(
    'chat', meta,
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('name', sa.String(64), nullable=False, unique=True),

    sa.PrimaryKeyConstraint('id', name='chat_id_pkey')
)
message = sa.Table(
    'message', meta,
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('chat_id', sa.Integer, nullable=False),
    sa.Column('message', sa.String(256), nullable=False),

    sa.PrimaryKeyConstraint('id', name='message_id_pkey'),
    sa.ForeignKeyConstraint(['chat_id'], [chat.c.id], name='chat_id_fkey', ondelete='CASCADE')
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
