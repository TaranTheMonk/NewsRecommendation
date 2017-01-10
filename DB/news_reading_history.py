from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
import os

Base = declarative_base()

class ReadingHistory(Base):
    __tablename__ = 'news_reading_history'

    def __init__(self, device_id, list):
        self.device_id = device_id
        self.list = list

    device_id = Column(String, primary_key=True)
    list = Column(String)


def insert_news_reading_history(session, nrhs, bulksize=1000):
    if len(nrhs) > bulksize:
        insert_news_reading_history(session, nrhs[bulksize:], bulksize)
        nrhs = nrhs[:bulksize]
    if len(nrhs) == 0:
        return
    sqlb = "INSERT INTO recommend_system.news_reading_history (device_id, list) VALUES"
    sqldata = ','.join("('%s', '%s')" % (nrh.device_id, nrh.interest) for nrh in nrhs)
    sqle = ' ON DUPLICATE KEY UPDATE list=values(list)'
    session.execute(''.join([sqlb, sqldata, sqle]))
    session.commit()

def insert_news_reading_history_from_file(session, filename, bulksize=1000):
    if not os.path.exists(filename):
        return
    nrhs = []
    with open(filename, 'r') as f:
        for row in f:
            col = row.split('\t')
            if len(col) == 2:
                nrhs.append(ReadingHistory(col[0], col[1]))
    f.close()
    insert_news_reading_history(session, nrhs)


