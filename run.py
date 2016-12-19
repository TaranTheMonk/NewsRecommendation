from DB.news import *
import argparse

def main():
	parser = argparse.ArgumentParser(description='Recommendation calculation')
	parser.add_argument('--dev', action='store_const', const=True)
	parser.add_argument('--prod', action='store_const', const=True)
	args = parser.parse_args()
	if not args.dev and not args.prod:
		parser.print_help()
		return 
	mysql_url = 'mysql://HSDBADMIN:NestiaHSPWD@hsdb.cd29ypfepkmi.ap-southeast-1.rds.amazonaws.com:3306/news'
	if args.prod:
		mysql_url = 'mysql://nestia_food:nestiafood002233@prod-mysql-nestia-food.cd29ypfepkmi.ap-southeast-1.rds.amazonaws.com:3306/news'
	db_engine = create_engine(mysql_url, echo=True)
	session = sessionmaker(bind=db_engine)()

	#saving all news data
	news_list = read_all_news(session)
	save_all_news(news_list, "./RecommendationSys/data/news_all.json")



main()