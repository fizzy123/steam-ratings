import requests
import os
import re
import json

def import_ratings():
    response = requests.get('http://api.steampowered.com/ISteamApps/GetAppList/v0001/')
    data = response.json()
    apps = data['applist']['apps']['app']
    apps = filter(lambda x: not re.search(r' Demo$| Pack| Beta$| Server$| Trailer| Test$| DLC| Soundtrack$| Content$| OST$| Skin$| Teaser| Press Review$| Editor| server$| Video$| Bundle', x['name']), apps)

    cookie = {'birthtime':'220953601'}

    for app in apps:
        try:
            response = requests.get('http://store.steampowered.com/app/{}/'.format(app['appid']), cookies=cookie)
        except Exception as e:
            continue
        print(response.content)
        ratings = re.findall(r"user_reviews_count\">\(([0-9,]+)", response.content)
        print("\n")
        print(repr(app['name']))
        print(app['appid'])
        print(apps.index(app))
        print(ratings)
        if len(ratings):
            if ratings[2] == '0':
                app['ratio'] = float('inf')
                app['good'] = int(ratings[1].replace(',',''))
                app['bad'] = int(ratings[2].replace(',',''))
            else:
                app['ratio'] = float(ratings[1].replace(',','')) / float(ratings[2].replace(',',''))
                app['good'] = int(ratings[1].replace(',',''))
                app['bad'] = int(ratings[2].replace(',',''))
            print(app['ratio'])
            print(app['good'])
            print(app['bad'])
        with open('steam_games.json', 'w') as f:
            json.dump(apps, f)

    games = filter(lambda x: 'ratio' in x, apps)

print("/n")
print("BEST REGULAR GAMES")
normal_games = filter(lambda x: x['bad'], games)
print sorted(normal_games, key=lambda game: game['ratio'])[0:10]

print("/n")
print("BEST NO BAD REVIEW GAMES")
inf_games = filter(lambda x: not x['bad'], games)
print sorted(inf_games, key=lambda game: game['good'])[0:10]
