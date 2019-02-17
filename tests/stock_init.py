import pandas as pd
import sqlalchemy

from abuui.abuui import settings


def create_engine():
    user = settings.DATABASES['default']['USER']
    password = settings.DATABASES['default']['PASSWORD']
    database_name = settings.DATABASES['default']['NAME']
    host = settings.DATABASES['default']['HOST']
    port = settings.DATABASES['default']['PORT']

    database_url = 'mysql+mysqldb://{user}:{password}@{host}:{port}/{database_name}?charset=utf8'.format(
        user=user,
        host=host,
        port=port,
        password=password,
        database_name=database_name,
    )

    engine = sqlalchemy.create_engine(database_url)

    return engine


def init():
    stock_pd = pd.read_csv('/Users/bailijiang/work/01_code/github/python/xadmin/abuui/resource/stock_code_CN.csv')

    stock_pd = stock_pd.drop(['Unnamed: 0'], axis=1)

    print(stock_pd.tail())

    stock_pd['symbol_str'] = stock_pd['symbol']

    stock_pd['symbol'].astype('str')

    print(stock_pd.info())

    stock_pd['symbol'] = stock_pd['symbol'].apply(lambda x: str(x).rjust(6, '0'))
    print(stock_pd.tail())
    stock_pd.to_sql('test_stock', create_engine(), if_exists='append', index=False, chunksize=2000)


init()
