import re
import json
import requests
from datetime import datetime
import multiprocessing
import time

from steam_ratings.models import GameInfo
from steam_ratings import db

COOKIE = {'birthtime':'220953601'}

def import_data():
    response = requests.get('http://api.steampowered.com/ISteamApps/GetAppList/v0001/')
    data = response.json()
    apps = data['applist']['apps']['app']
# pylint: disable=line-too-long
    apps = list(filter(lambda x: not re.search(r' Demo$| Pack| Beta$| Server$| Trailer| Test$| DLC| Soundtrack$| Content$| OST$| Skin$| Teaser| Press Review$| Editor| server$| Video$| Bundle| Add-On$', x['name']), apps))
    with open('steam_games.json', 'w') as f:
        json.dump(apps, f)

    pool = multiprocessing.Pool()
    result = pool.map_async(process_app, apps, chunksize=1)
    while not result.ready():
        print("num left: {}".format(result._number_left))
        time.sleep(15)
    pool.close()
    pool.join()

    print("UPDATED ON {}".format(datetime.today().strftime('%Y-%m-%d')))

def process_app(app):
    try:
        url = 'http://store.steampowered.com/app/{}/'.format(app['appid'])
        response = requests.get(url, cookies=COOKIE)
        if response.url.split('/')[-2] != str(app['appid']):
            return
        if re.search(r"<h1>Downloadable Content</h1>", response.text):
            return
    except Exception as e:
        print("Encountered error {} on {}".format(e, app))
        return
    ratings = re.findall(r"user_reviews_count\">\(([0-9,]+)", response.text)
    if ratings:
        print("Ratings found for {}".format(app['name']))
        try:
            if ratings[2] == '0':
                app['ratio'] = float('inf')
                app['good'] = int(ratings[1].replace(',', ''))
                app['bad'] = int(ratings[2].replace(',', ''))
            else:
                app['ratio'] = float(ratings[1].replace(',', '')) / float(ratings[2].replace(',', ''))
                app['good'] = int(ratings[1].replace(',', ''))
                app['bad'] = int(ratings[2].replace(',', ''))
            game_info = GameInfo.query.filter(GameInfo.game_id == app['appid']).first()
            if game_info:
                print("Updating {}".format(game_info.name))
                game_info.good = app['good']
                game_info.bad = app['bad']
                game_info.ratio = app['ratio']
                game_info.total = app['good'] + app['bad']
                game_info.online_coop = len(re.findall(r">Online Co-op<", response.text)) != 0
                game_info.local_coop = len(re.findall(r">Shared/Split Screen Co-op<", response.text)) != 0
            else:
                game_info = GameInfo(game_id=app['appid'], name=app['name'], good=app['good'], bad=app['bad'], online_coop=len(re.findall(r">Online Co-op<", response.text)) != 0, local_coop=len(re.findall(r">Shared/Split Screen Co-op<", response.text)) != 0)
                db.session.add(game_info)
            game_info.tags = re.findall(r"class=\"app_tag\" style=\"display: none;\">[\s]+([A-z]+)[\s]+<\/a>", response.text)
            db.session.commit()
        except Exception as e:
            print("Encountered error {} on {}".format(e, app))
            return
    else:
        print("No ratings found for {}".format(app["name"]))
    return
