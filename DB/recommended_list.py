from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine
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

def insert_recommended_list(session, recs, bulksize):
	if len(recs) > bulksize: 
		insert_recommended_list(recs[bulksize:], bulksize)
		recs = recs[:bulksize]
	if len(recs) == 0:
		return 
	sql = "INSERT INTO recommended_list (device_id, list) VALUES ('%s', '%s')" % (recs[0].device_id, recs[0].recommended_list)
	for rec in recs:
		sql = sql + ", ('%s', '%s')" % (rec.device_id, rec.recommended_list)
	sql = sql + "ON DUPLICATE KEY UPDATE list=values(list)"
	session.execute(sql)
	session.commit()


def rec_test():
	db_engine = create_engine('mysql://HSDBADMIN:NestiaHSPWD@hsdb.cd29ypfepkmi.ap-southeast-1.rds.amazonaws.com:3306/news', echo=True)
	session = sessionmaker(bind=db_engine)()
	recs = [RecommendedList("chinese", "[82,387,8864,59,112,318,8865,387,40,456,300,194,11,162,89,228,274,211,445,237,106,495,466,28,258,47,447,287,388,290,15,41,408,387,331,429]"),
		RecommendedList("english", "[82,387,8864,59,112,318,8865,387,40,456,300,194,11,162,89,228,274,211,445,237,106,495,466,28,258,47,447,287,388,290,15,41,408,387,331,429]")]
	insert_recommended_list(session, recs, 100)
