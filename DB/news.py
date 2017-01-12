from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
import jsonpickle
from datetime import datetime, timedelta

Base = declarative_base()
RevealMode = {
    0: 0, 15: 1, 16: 1, 18: 1, 19: 1, 20: 1, 21: 1,
    22: 1, 23: 1, 24: 1, 25: 1, 26: 1, 27: 1, 28: 1,
    1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1, 8: 1,
    9: 1, 10: 1, 11: 1, 12: 1, 13: 1, 14: 1, 17: 1
}


class News(Base):
    __tablename__ = "news"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    content = Column(String)
    type = Column(Integer)
    published_at = Column(DateTime)
    language_id = Column(Integer)
    status = Column(Integer)
    time_bound = Column(Integer)
    source_site = Column(Integer)


def read_all_news(session):
    return session.query(News).filter(News.published_at > datetime.now() - timedelta(days=30)).all()


def save_all_news(news_list, file_path):
    file = open(file_path, 'w')
    new_list = []
    for news in news_list:
        newsmp  = {
            'id': news.id,
            'title': news.title,
            'content': news.content,
            'type': news.type,
            'published_at': news.published_at.strftime("%Y-%m-%dT%H:%M:%SZ"),
            'language_id': news.language_id,
            'status': news.status,
            'time_bound': news.time_bound,
            'reveal_mode': 2,
        }
        if news.source_site in RevealMode:
            newsmp['reveal_mode'] = RevealMode[news.source_site]
        new_list.append(newsmp)
    file.write(jsonpickle.encode(new_list))
    file.close()


# def news_test():
#     db_engine = create_engine(
#         'mysql://HSDBADMIN:NestiaHSPWD@hsdb.cd29ypfepkmi.ap-southeast-1.rds.amazonaws.com:3306/news', echo=True)
#     session = sessionmaker(bind=db_engine)()
#     news_list = read_all_news(session)
#     save_all_news(news_list, "./news_all.json")
