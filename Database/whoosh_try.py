from datetime import datetime
import flask_sqlalchemy
import flask_whooshalchemy
from whoosh.analysis import StemmingAnalyzer
from flask import Flask
app=Flask(__name__)
app.config['WHOOSH_BASE'] = 'try1'

db = flask_sqlalchemy.SQLAlchemy()

class BlogPost(db.Model):
    __tablename__ = 'posts'
    __searchable__ = ['title', 'content', 'summary'] # indexed fields
    __analyzer__ = StemmingAnalyzer()

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), unique=True)
    content = db.Column(db.Text(32*1024))
    summary = db.Column(db.String(1024))
    created = db.Column(db.DateTime, default=datetime.utcnow)

flask_whooshalchemy.whoosh_index(app, BlogPost)
with app.app_context():
    db.session.add(BlogPost(title='First Post!', content='This is awesome.'))
    db.session.commit()

    db.session.add(user)
    db.session.commit()

from sqlalchemy.databases import whoosh_index