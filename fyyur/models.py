from fyyur import db



#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

GenreVenue = db.Table(
  'genre_venue',
  db.Column('venue_id', db.Integer, db.ForeignKey('venues.id'), primary_key=True, nullable=False),
  db.Column('genre_id', db.Integer, db.ForeignKey('genres.id'), primary_key=True, nullable=False)
)

ArtistGenre = db.Table(
  'artist_genre',
  db.Column('artist_id', db.Integer, db.ForeignKey('artists.id'), primary_key=True, nullable=False),
  db.Column('genre_id', db.Integer, db.ForeignKey('genres.id'), primary_key=True, nullable=False)
)

class Venue(db.Model):
    __tablename__ = 'venues'

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
    shows = db.relationship('Show', backref='Show', lazy=True)
    created_at =db.Column(db.DateTime, nullable=True,)
    updated_at =db.Column(db.DateTime, nullable=True,)
    

class Artist(db.Model):
    __tablename__ = 'artists'

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
    created_at =db.Column(db.DateTime, nullable=True,)
    updated_at =db.Column(db.DateTime, nullable=True,)
    

class Show(db.Model):
  __tablename__ = 'shows'
  
  id = db.Column(db.Integer, primary_key=True)
  artist_id = db.Column(db.Integer, db.ForeignKey('artists.id'), nullable=False)
  venue_id = db.Column(db.Integer, db.ForeignKey('venues.id'), nullable=False)
  start_time = db.Column(db.DateTime, nullable=True)
  created_at =db.Column(db.DateTime, nullable=True,)
  updated_at =db.Column(db.DateTime, nullable=True,)


class Genre(db.Model):
  __tablename__ = 'genres'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String)
  created_at =db.Column(db.DateTime, nullable=True,)
  updated_at =db.Column(db.DateTime, nullable=True,)
