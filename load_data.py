from contextlib import contextmanager

import pandas as pd
from clickhouse_sqlalchemy.types import *
from sqlalchemy import create_engine, Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class Domain(Base):
    __tablename__ = 'domain'
    id = Column(Int64, primary_key=True)
    name = Column(String)

    def to_dict(self):
        return {col.name: getattr(self, col.name) for col in self.__table__.columns}


class SqlCommon:
    def __init__(self):
        self.engine = create_engine(
            'clickhouse://X_Force:Ir2OFknR2hQDrXFVD2Ie@phoenix-db.data.tripi.vn:443/PhoeniX?protocol=https',
            echo=False,
            pool_recycle=600,
            pool_pre_ping=True,
            max_overflow=10
        )
        self.session = sessionmaker(bind=self.engine)

    @contextmanager
    def get_session(self, auto_commit=True):
        my_session = self.session()
        try:
            yield my_session
            if auto_commit:
                my_session.commit()
        except Exception as e:
            my_session.rollback()
            raise e
        finally:
            my_session.close()

    def get_engine(self):
        return self.engine

    def execute(self, sql):
        return self.get_engine().execute(f'{sql} FORMAT TabSeparatedWithNamesAndTypes')


# phoenix_db = SqlCommon()

# if __name__ == '__main__':
# #     # with phoenix_db.get_session() as session:
# #     #     domains = session.query(Domain).all()
# #     # print(f'size: {len(domains)}')
#     df = pd.DataFrame(phoenix_db.execute('select * from hotel_price_daily limit 100'))#, columns=['id', 'hotel_id', 'domain_id', 'domain_hotel_id', 'cosine_name', 'cosine_address', 'distance', 'similar_point', 'rank_point', 'created_date_id', 'created_datetime'])
#     print(df)
