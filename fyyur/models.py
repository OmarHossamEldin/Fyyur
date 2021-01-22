from fyyur import db


# time zone for creationTime
from datetime import datetime
import pytz
tz = pytz.timezone('Africa/Cairo')
ct = datetime.now(tz=tz)
#time zone for creationTime

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

GenreVenue = db.Table(
  'GenreVenue',
  db.Column('venue_id', db.Integer, db.ForeignKey('Venue.id'), primary_key=True, nullable=False),
  db.Column('genra_id', db.Integer, db.ForeignKey('Genre.id'), primary_key=True, nullable=False)
)

ArtistGenre = db.Table(
  'ArtistGenre',
  db.Column('artist_id', db.Integer, db.ForeignKey('Artist.id'), primary_key=True, nullable=False),
  db.Column('genre_id', db.Integer, db.ForeignKey('Genre.id'), primary_key=True, nullable=False)
)

class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    address = db.Column(db.String(120))
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120),nullable=True)
    seeking_talent = db.Column(db.Boolean, default=True)
    website = db.Column(db.String(120))
    facebook_link = db.Column(db.String(120),default='https://www.facebook.com/theduelingpianos')
    image_link = db.Column(db.String(500), default='https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60')
    seeking_description = db.Column(db.Text,nullable=True)
    genres = db.relationship('Genre', secondary=GenreVenue,backref=db.backref('Venue', lazy=True))
    shows = db.relationship('Show', backref='hasShows', lazy=True)
    created_at =db.Column(db.DateTime, nullable=False, default=ct)
    updated_at =db.Column(db.DateTime, nullable=False, default=ct)
    

class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean, default=True)
    website = db.Column(db.String(120))
    facebook_link = db.Column(db.String(120))
    image_link = db.Column(db.String(500), default='https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80')
    seeking_description = db.Column(db.Text,nullable=True)
    shows = db.relationship('Show', backref='hasShows', lazy=True)
    genres = db.relationship('Genre', secondary=ArtistGenre,backref=db.backref('Artist', lazy=True))
    created_at =db.Column(db.DateTime, nullable=False, default=ct)
    updated_at =db.Column(db.DateTime, nullable=False, default=ct)
    

class Show(db.Model):
  __tablename__ = 'Show'
  
  id = db.Column(db.Integer, primary_key=True)
  artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'), nullable=False)
  venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'), nullable=False)
  start_time = db.Column(db.DateTime, nullable=True)
  shows = db.relationship('Show', backref='hasShows', lazy=True)
  created_at =db.Column(db.DateTime, nullable=False, default=ct)
  updated_at =db.Column(db.DateTime, nullable=False, default=ct)


class Genres(db.Model):
  __tablename__ = 'Genre'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String)

