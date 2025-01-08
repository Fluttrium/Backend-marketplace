from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import async_sessionmaker
import ssl
from app.config import settings

ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False  # Отключаем проверку имени хоста не ттрогать тронене все габела
ssl_context.verify_mode = ssl.CERT_NONE  # Отключаем проверку сертификата очень небнзопасно но ромман настоял

if settings.MODE == "TEST":
    DATABASE_URL = settings.TEST_DATABASE_URL
    DATABASE_PARAMS = {"poolclass": NullPool}
else:
    DATABASE_URL = settings.DATABASE_URL
    DATABASE_PARAMS = {}

engine = create_async_engine(DATABASE_URL, **DATABASE_PARAMS,
                             connect_args={"ssl": ssl_context},
                             echo=True
                             )


async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


async def get_db():
    async with async_session_maker() as session:
        yield session

class Base(DeclarativeBase):
    pass
