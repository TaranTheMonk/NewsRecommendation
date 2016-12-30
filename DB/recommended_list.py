from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class RecommendedList(Base):
    __tablename__ = "recommended_list"

    def __init__(self, device_id, recommended_list):
        self.device_id = device_id
        self.recommended_list = recommended_list

    device_id = Column(String, primary_key=True)
    recommended_list = Column('list', String)


def insert_recommended_list(session, recs, bulksize, lang):
    if len(recs) > bulksize:
        insert_recommended_list(recs[bulksize:], bulksize)
        recs = recs[:bulksize]
    if len(recs) == 0:
        return
    sqlb = "INSERT INTO recommended_list (device_id, language_id, list) VALUES "
    sqldata = ','.join("('%s', %s, '%s')" % (rec.device_id, str(lang), rec.recommended_list) for rec in recs)
    sqle = " ON DUPLICATE KEY UPDATE list=values(list), language_id=values(language_id)"
    session.execute(''.join([sqlb, sqldata, sqle]))
    session.commit()


def insert_rec_from_file(session, file_path, bulksize=100, lang=1):
    file = open(file_path, 'r')
    recs = []
    for line in iter(file.readline, ''):
        sp = line.split('\t', 1)
        if len(sp) == 2:
            recs.append(RecommendedList(sp[0], sp[1]))
        if len(recs) == bulksize:
            insert_recommended_list(session, recs, bulksize, lang)
            recs = []
    insert_recommended_list(session, recs, bulksize, lang)
    file.close()

def get_expired_device_ids(session):
    bulk = 1000
    ret = session.query(RecommendedList.device_id).filter(text('updated_at < DATE_SUB(now(), INTERVAL 6 hour)')).order_by(text('updated_at, device_id'))[:bulk]
    if len(ret) == 0:
        return ret
    session.execute('UPDATE recommended_list SET updated_at = NOW() WHERE device_id IN (%s)' % (','.join("'" + d[0] + "'" for d in ret)))
    session.commit()
    return ret