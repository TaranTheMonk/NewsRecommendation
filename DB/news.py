from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import jsonpickle

Base = declarative_base()

class News(Base):
	__tablename__ = "news"

	id = Column(Integer, primary_key=True)
	title = Column(String)
	content = Column(String)
	type = Column(Integer)
	published_at = Column(DateTime)
	language_id = Column(Integer)
	source_link = Column(String)

def read_all_news(session): 
	return session.query(News).filter(News.source_link=='').all()

def save_all_news(news_list, file_path):
	file = open(file_path, 'w')
	file.write(jsonpickle.encode(news_list))
	file.close()

def news_test(): 
	db_engine = create_engine('mysql://HSDBADMIN:NestiaHSPWD@hsdb.cd29ypfepkmi.ap-southeast-1.rds.amazonaws.com:3306/news', echo=True)
	session = sessionmaker(bind=db_engine)()
	news_list = read_all_news(session)
	save_all_news(news_list, "./news_all.json")


