from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
import os

Base = declarative_base()

class UserInfo(Base):
    __tablename__ = "user_data"

    def __init__(self, device_id, interest, language_id):
        self.device_id = device_id
        self.interest = interest
        self.language_id = language_id

    device_id = Column(String, primary_key=True)
    interest = Column(String)
    language_id = Column(Integer)

def insert_user_info(session, infos, bulksize=1000):
    if len(infos) > bulksize:
        insert_user_info(session, infos[bulksize:], bulksize)
        infos = infos[:bulksize]
    if len(infos) == 0:
        return
    sqlb = "INSERT INTO recommend_system.user_data (device_id, interest, language_id) VALUES"
    sqldata = ','.join("('%s', '%s', %d)" % (info.device_id, info.interest, info.language_id) for info in infos)
    sqle = ' ON DUPLICATE KEY UPDATE interest=values(interest), language_id=values(language_id)'
    session.execute(''.join([sqlb, sqldata, sqle]))
    session.commit()

def insert_user_info_from_file(session, filename, bulksize=1000):
    if not os.path.exists(filename):
        return
    infos = []
    with open(filename, 'r') as f:
        for row in f:
            col = row.split('\t')
            if len(col) == 3:
                infos.append(UserInfo(col[0], col[1], int(col[2])))
    f.close()
    insert_user_info(session, infos)
