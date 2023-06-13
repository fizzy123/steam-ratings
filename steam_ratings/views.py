import logging
import urllib
from sqlalchemy.sql import operators

from flask import render_template, request, jsonify

from steam_ratings import app
from steam_ratings.models import GameInfo

logger = logging.getLogger(__name__)

@app.route('/')
def index_view():
    return render_template('index.html')

@app.route('/games', methods=['GET'])
def games_view():
    query = GameInfo.query
    if request.args.get('min_good'):
        query = query.filter(GameInfo.good > request.args.get('min_good'))
    if request.args.get('min_bad', 1):
        query = query.filter(GameInfo.bad > request.args.get('min_bad', 1))
    if request.args.get('min_total', 500):
        query = query.filter(GameInfo.total > request.args.get('min_total', 500))
    if request.args.get('min_ratio'):
        query = query.filter(GameInfo.ratio < request.args.get('min_ratio'))

    if request.args.get('max_good'):
        query = query.filter(GameInfo.good < request.args.get('max_good'))
    if request.args.get('max_bad'):
        query = query.filter(GameInfo.bad < request.args.get('max_bad'))
    if request.args.get('max_total'):
        query = query.filter(GameInfo.total < request.args.get('max_total'))
    if request.args.get('max_ratio'):
        query = query.filter(GameInfo.ratio < request.args.get('max_ratio'))
    if request.args.get('local_coop'):
        query = query.filter(GameInfo.local_coop == request.args.get('local_coop'))
    if request.args.get('online_coop'):
        query = query.filter(GameInfo.online_coop == request.args.get('online_coop'))
    if request.args.get('include_tags'):
        for tag in urllib.parse.unquote(request.args.get('include_tags')).split(','):
            query = query.filter(GameInfo.tags.any(tag))
    if request.args.get('exclude_tags'):
        for tag in urllib.parse.unquote(request.args.get('exclude_tags')).split(','):
            query = query.filter(GameInfo.tags.all(tag, operator=operators.ne))

    if request.args.get('increasing'):
        query = query.order_by(GameInfo.ratio)
    else:
        query = query.order_by(GameInfo.ratio.desc())
    page = int(request.args.get('page', 1))

    pagination = query.paginate(page=page, per_page=50)
    games = pagination.items
    return jsonify({'games': [game.dictify() for game in games], 'total': pagination.pages})
