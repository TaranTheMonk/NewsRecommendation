from DB.news import *
from DB.recommended_list import *
import argparse
import os
import time
import re
import sys
from datetime import datetime, timedelta


def move_log_file():
    os.system('mkdir -p ~/.recsys/Data/Input')
    os.system('mv -f ~/.recsys/nestia_logs/data-%s.csv ~/.recsys/Data/Input/input.csv' % (
    datetime.utcnow() - timedelta(hours=2)).strftime("%Y-%m-%d-%H"))


def run_timer_task(session, moment):
    while True:
        if datetime.utcnow().strftime("%M:%S") == moment:
            run(session)
        else:
            moment_min = int(moment.split(':')[0])
            if datetime.utcnow().second % 60 == 0 and (moment_min + 55 - datetime.utcnow().minute) % 60 > 5:
                run_random_only(session)
        print(datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"))
        sys.stdout.flush()
        time.sleep(1)


def read_from_config():
    parser = argparse.ArgumentParser(description='Recommendation calculation. Kindly use '
                                                 '[python run.py --dev --time 30:00]')
    parser.add_argument('--dev', action='store_const', const=True,
                        help='Run this in dev mode. (Required without --prod)')
    parser.add_argument('--prod', action='store_const', const=True,
                        help='Run this in prod mode. (Required without --dev)')
    parser.add_argument('--time', nargs='?', default='30:00', help='Time moment to run. (30:00)')
    args = parser.parse_args()
    if not args.dev and not args.prod:
        parser.print_help()
        return
    if not re.compile('^[0-5][0-9]:[0-5][0-9]$').match(args.time):
        print('Time format wrong. ')
        return

    mysql_url = 'mysql://HSDBADMIN:NestiaHSPWD@hsdb.cd29ypfepkmi.ap-southeast-1.rds.amazonaws.com:3306/news'
    if args.prod:
        mysql_url = 'mysql://nestia_food:nestiafood002233@prod-mysql-nestia-food.cd29ypfepkmi.ap-southeast-1.rds.amazonaws.com:3306/news'
    db_engine = create_engine(mysql_url)
    session = sessionmaker(bind=db_engine)()
    run_timer_task(session, args.time)


def run(session):
    # saving all news data
    news_list = read_all_news(session)
    os.system('mkdir -p ~/.recsys/Data/TestDocs')
    save_all_news(news_list, os.path.expanduser("~/.recsys/Data/TestDocs/news_all.json"))

    move_log_file()

    import RecommendationSys.src.CosSimilarity as cos_sim
    cos_sim.main()

    import RecommendationSys.src.UpdateMatrix as update_matrix
    update_matrix.main()

    import RecommendationSys.src.Main as result_saver
    result_saver.SaveOutput()

    insert_rec_from_file(session, os.path.expanduser('~/.recsys/Data/Output/device_result.tsv'))


def run_random_only(session):
    device_ids = get_expired_device_ids(session)
    if len(device_ids) == 0:
        return
    os.system('mkdir -p ~/.recsys/Data/ConfigData')
    with open(os.path.expanduser('~/.recsys/Data/ConfigData/ActiveUser.csv'), 'w') as file:
        for device_id in device_ids:
            file.write(device_id[0] + '\n')
    file.close()
    import RecommendationSys.src.Main as result_saver
    result_saver.SaveOutput()
    insert_rec_from_file(session, os.path.expanduser('~/.recsys/Data/Output/device_result.tsv'))
    print('Shuffle finished')

read_from_config()
