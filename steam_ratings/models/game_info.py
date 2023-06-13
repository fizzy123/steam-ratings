from steam_ratings import db

class GameInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(), nullable=False)
    good = db.Column(db.Integer, nullable=False)
    bad = db.Column(db.Integer, nullable=False)
    total = db.Column(db.Integer, nullable=False)
    ratio = db.Column(db.Float, nullable=False)
    local_coop = db.Column(db.Boolean, nullable=False, default=False)
    online_coop = db.Column(db.Boolean, nullable=False, default=False)
    tags = db.Column(db.ARRAY(db.String()))

    def __init__(self, game_id, name, good, bad, local_coop, online_coop):
        self.game_id = game_id
        self.name = name
        self.good = good
        self.bad = bad
        if bad != 0:
            self.ratio = good/bad
        else:
            self.ratio = float('inf')
        self.total = good + bad
        self.local_coop = local_coop
        self.online_coop = online_coop

    def dictify(self):
        return {
            'id': self.id,
            'game_id': self.game_id,
            'name': self.name,
            'good': self.good,
            'bad': self.bad,
            'ratio': self.ratio,
            'total': self.total,
            'local_coop': self.local_coop,
            'online_coop': self.online_coop,
            'tags': self.tags
        }

    def __repre__(self):
        return '<GameInfo %r>' % self.name
