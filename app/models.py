__author__ = 'Ahuja'
from app import db
from sqlalchemy.dialects.postgresql import JSON
# This configures the database. You need to set the env variable DB_HOST for it to work.
# the db host should be the url of

class Skill(db.Model):
    __tablename__ = 'skill_occurance'
    id          = db.Column(db.Integer,nullable=False,primary_key=True)
    keyword     = db.Column(db.String(255),nullable=False)
    category    = db.Column(db.String(255))
    industry    = db.Column(db.String(255))
    title       = db.Column(db.String(255))
    onet_title  = db.Column(db.String(255))
    c_title     = db.Column(db.String(255))
    state       = db.Column(db.String(255))
    city        = db.Column(db.String(255))
    created     = db.Column(db.DateTime)

    def __init__(self, keyword, category, industry, title, onet_title, c_title, state, city, created):
        self.keyword = keyword
        self.category = category
        self.industry = industry
        self.title = title
        self.onet_title = onet_title
        self.c_title = c_title
        self.state = state
        self.city = city
        self.created = created

    def __repr__(self):
        return '<skill {}>'.format(self)