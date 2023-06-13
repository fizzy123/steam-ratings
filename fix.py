import re
import requests

from steam_ratings.models import GameInfo
from steam_ratings import db
games = GameInfo.query.all()
for game in games:
    print(game.name)
    url = 'http://store.steampowered.com/app/{}/'.format(game.game_id)
    response = requests.get(url)
    if response.url.split('/')[-2] != str(game.game_id) or re.search(r"<h1>Downloadable Content</h1>", response.text):
        db.session.delete(game)
db.session.commit()
