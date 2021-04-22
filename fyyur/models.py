from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask import Flask

app = Flask(__name__)
db = SQLAlchemy(app)
migrate = Migrate(app, db)


#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    genres = db.Column(db.ARRAY(db.String(120)),default="Music",nullable=False)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120),unique=True)
    phone = db.Column(db.String(120),unique=True)
    image_link = db.Column(db.String(500))
    website = db.Column(db.String(120),unique=True)
    facebook_link = db.Column(db.String(120),unique=True)
    seeking_talent=db.Column(db.Boolean(),default=False,nullable=False)
    seeking_description = db.Column(db.String(500))
    # past_shows=db.Column(db.Integer(),db.ForeignKey('Shows.id'))

    # TODO: implement any missing fields, as a database migration using Flask-Migrate

class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120),unique=True)
    genres = db.Column(db.ARRAY(db.String(120)),default="Music",nullable=False)
    image_link = db.Column(db.String(500))
    website = db.Column(db.String(120),unique=True)
    facebook_link = db.Column(db.String(120),unique=True)
    seeking_venue=db.Column(db.Boolean(),default=False,nullable=False)
    seeking_description = db.Column(db.String(500))
    # past_shows = db.Column(db.Integer(), db.ForeignKey('Shows.id'))

    # TODO: implement any missing fields, as a database migration using Flask-Migrate
    


# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.
class Shows(db.Model):
  __tablename__ = 'Shows'
  id = db.Column(db.Integer, primary_key=True)
  name=db.Column(db.String(120))
  artist_id=db.Column(db.Integer(),db.ForeignKey('Artist.id'))
  venue_id=db.Column(db.Integer(),db.ForeignKey('Venue.id'))
  start_time=db.Column(db.DateTime)

  


