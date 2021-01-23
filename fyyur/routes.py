
from fyyur import app
from flask import render_template, request, Response, flash, redirect, url_for
from fyyur.forms import *
from fyyur.models import *


#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format)

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')

#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  venues = db.session.query(
    Venue.id, Venue.name, Venue.city, Venue.state, db.func.count(Show.venue_id)).outerjoin(
    Show, Venue.id == Show.venue_id and Show.start_time > datetime.now()).group_by(
    Venue.id,Venue.name,Venue.city,Venue.state).distinct(Venue.city,Venue.state).all()
  keys = ["id", "name", "city", "state", "num_upcoming_shows"]
  data = []
  for venue in venues:
    data.append(dict( zip(keys, venue) ))
  return render_template('pages/venues.html',title = 'Venues', areas=data)

@app.route('/venues/search', methods=['POST'])
def search_venues(): 
  search_term = request.form.get('search_term').strip()
  venues = Venue.query.filter(Venue.name.ilike(f'%{search_term}%')).all()
  data = []
  for venue in venues:
     data.append({
            "id": venue.id,
            "name": venue.name,
        })
  response = {
        "count": len(venues),
        "data": data
    }
  flash('Got results','success')
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  venues = Venue.query.get_or_404(venue_id)
  genres = []
  current_time = datetime.now()
  past_shows = []
  past_shows_count = 0
  upcoming_shows = []
  upcoming_shows_count = 0  
    
  for genre in venues.genres:
    genres.append(genre.name)
    
  for show in venues.shows:
      if show.start_time >= current_time:
        upcoming_shows_count += 1
        upcoming_shows.append({
          "artist_id":show.artist_id,
          "artist_name":show.artist.name,
          "start_time":format_datetime(str(show.start_time)),
          "artist_image_link":show.artist.image_link
        })
      elif show.start_time < current_time:
        past_shows_count += 1
        past_shows.append({
          "artist_id": show.artist_id,
          "artist_name": show.artist.name,
          "start_time": format_datetime(str(show.start_time)),
          "artist_image_link": show.artist.image_link
        })  
  data = {
            "id": venues.id,
            "name": venues.name,
            "city": venues.city,
            "state": venues.state,          
            "address": venues.address,
            "phone": venues.phone,
            "image_link": venues.image_link,
            "facebook_link": venues.facebook_link,
            "website": venues.website,
            "seeking_talent": venues.seeking_talent,
            "seeking_description": venues.seeking_description,
            "genres": genres,
            "past_shows": past_shows,
            "past_shows_count": past_shows_count,
            "upcoming_shows": upcoming_shows,
            "upcoming_shows_count": upcoming_shows_count          
  }  
  return render_template('pages/show_venue.html',title = 'Venue Search', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', title='New Venue',form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  form = VenueForm()
  if form.validate_on_submit():
    venue = Venue(
      name=form.name.data,
      address=form.address.data,
      city=form.city.data,
      state=form.state.data,
      phone=form.phone.data,
      seeking_talent=form.seeking_talent.data,
      website=form.website.data,
      facebook_link=form.facebook_link.data,
      image_link=form.image_link.data,
      seeking_description=form.seeking_description.data,
      created_at='now()',
      updated_at='now()',
      )
    db.session.add(venue)
    venueGenres =form.genres.data
    venueGenres =venueGenres.split('-')
    for value in venueGenres:
      genre = Genre.query.filter_by(name = value).first()
      if genre:
        venue.genres.append(genre)
      else:
        genre = Genre(name = value, created_at = 'now()', updated_at = 'now()')
        db.session.add(genre)
        venue.genres.append(genre)
    db.session.commit()
    db.session.close()
    flash(f"Venue {request.form['name']} was successfully listed!",'success')
    return redirect(url_for('venues'))
  else:
    flash(f"An error occurred. Venue {request.form['name']} could not be listed.",'danger')
    return render_template('forms/new_venue.html', title='New Venue',form=form)
  
@app.route('/venues/<venue_id>', methods=['POST'])
def delete_venue(venue_id):
  venue = Venue.query.get_or_404(venue_id)
  try:
    db.session.delete(venue)
    db.session.commit()
    flash(f'venue deleted Successfully','success')
    return redirect(url_for('index'))
  except:
    db.session.rollback()

    flash(f' error occurred on deleting venue','danger')
    return redirect(url_for('index'))
  finally:
    db.session.close() 


#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  data = []
  artists = Artist.query.all()  
  for artist in artists:
    data.append({
      "id": artist.id,
      "name": artist.name
      })
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  data = []
  search_term = request.form.get('search_term').strip()
  artists = Artist.query.filter(Artist.name.ilike('%' + search_term + '%')).all()
  for artist in artists:
     data.append({
            "id": artist.id,
            "name": artist.name,
        })
  response = {
        "count": len(artists),
        "data": data
  }
  return render_template('pages/search_artists.html',title = 'Artist Search', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  artist = Artist.query.get_or_404(artist_id)
  genres = []
  current_time = datetime.now()
  past_shows = []
  past_shows_count = 0
  upcoming_shows = []
  upcoming_shows_count = 0  
  for genre in artist.genres:
      genres.append(genre.name)

  for show in artist.shows:
      if show.start_time >= current_time:
        upcoming_shows_count += 1
        upcoming_shows.append({
          "artist_id":show.artist_id,
          "artist_name":show.Artist.name,
          "start_time":format_datetime(str(show.start_time)),
          "artist_image_link":show.Artist.image_link
        })
      elif show.start_time < current_time:
        past_shows_count += 1
        past_shows.append({
          "artist_id": show.artist_id,
          "artist_name": show.Artist.name,
          "start_time": format_datetime(str(show.start_time)),
          "artist_image_link": show.Artist.image_link
        })  
  data ={
          "id": artist.id,
          "name": artist.name,
          "city": artist.city,
          "state": artist.state,          
          "phone": artist.phone,
          "image_link": artist.image_link,
          "facebook_link": artist.facebook_link,
          "website": artist.website,
          "seeking_venue": artist.seeking_venue,
          "seeking_description": artist.seeking_description,
          "genres": genres,
          "past_shows": past_shows,
          "past_shows_count": past_shows_count,
          "upcoming_shows": upcoming_shows,
          "upcoming_shows_count": upcoming_shows_count          
  }
  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  artist = Artist.query.get_or_404(artist_id)
  genres=''
  for genre in artist.genres:
    genres += genre.name + '-'
  return render_template('forms/edit_artist.html', title= 'Edit Artist', form=form, artist=artist, genres = genres)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  artist = Artist.query.get_or_404(venue_id)
  form = ArtistForm()
  if form.validate_on_submit():

    artist.name = form.name.data,
    artist.city = form.city.data,
    artist.state = form.state.data,
    artist.phone = form.phone.data,
    artist.seeking_venue = form.seeking_venue.data,
    artist.website = form.website.data,
    artist.facebook_link = form.facebook_link.data,
    artist.image_link = form.image_link.data,
    artist.seeking_description = form.seeking_description.data,
    artist.updated_at = 'now()',

    db.session.add(artist)
    artistGenres =form.genres.data
    artistGenres =artistGenres.split('-')
    for value in artistGenres:
      genre = Genre.query.filter_by(name = value).first()
      if genre:
        artist.genres.append(genre)
      else:
        genre = Genre(name = value, created_at = 'now()', updated_at = 'now()')
        db.session.add(genre)
        artist.genres.append(genre)
    db.session.commit()
    db.session.close()
    flash(f"Artist {request.form['name']} updated successfully!",'success')
    return redirect(url_for('artists'))
  else:
    flash(f"An error occurred. Artist {request.form['name']} could not be updated.",'danger')
    return render_template('forms/edit_artist.html',title='edit Artist', form=form)

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  venue = Venue.query.get_or_404(venue_id)
  form = VenueForm()
  genres=''
  for genre in venue.genres:
    genres += genre.name + '-'
  return render_template('forms/edit_venue.html', title =  'Edit Venue', form=form, genres = genres, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  venue = Venue.query.get_or_404(venue_id)
  form = VenueForm()
  if form.validate_on_submit():
    venue.name = form.name.data
    venue.address = form.address.data
    venue.city = form.city.data
    venue.state = form.state.data
    venue.phone = form.phone.data
    venue.seeking_talent = form.seeking_talent.data
    venue.website = form.website.data
    venue.facebook_link = form.facebook_link.data
    venue.image_link = form.image_link.data
    venue.seeking_description = form.seeking_description.data
    venue.updated_at = 'now()'
    
    db.session.add(venue)
    venueGenres =form.genres.data
    venueGenres =venueGenres.split('-')
    for value in venueGenres:
      genre = Genre.query.filter_by(name = value).first()
      if genre:
        venue.genres.append(genre)
      else:
        genre = Genre(name = value, created_at = 'now()', updated_at = 'now()')
        db.session.add(genre)
        venue.genres.append(genre)
    db.session.commit()
    db.session.close()
    flash(f"Venue {request.form['name']} updated successfully!",'success')
    return redirect(url_for('venues'))
  else:
    flash(f"An error occurred. Venue {request.form['name']} could not be update.",'danger')
    return render_template('forms/edit_venue.html', title='edit Venue',form=form)
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html',title='New Artist', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  form = ArtistForm()
  if form.validate_on_submit():
    artist = Artist(
      name=form.name.data,
      city=form.city.data,
      state=form.state.data,
      phone=form.phone.data,
      seeking_venue=form.seeking_venue.data,
      website=form.website.data,
      facebook_link=form.facebook_link.data,
      image_link=form.image_link.data,
      seeking_description=form.seeking_description.data,
      created_at='now()',
      updated_at='now()',
      )
    db.session.add(artist)
    artistGenres =form.genres.data
    artistGenres =artistGenres.split('-')
    for value in artistGenres:
      genre = Genre.query.filter_by(name = value).first()
      if genre:
        artist.genres.append(genre)
      else:
        genre = Genre(name = value, created_at = 'now()', updated_at = 'now()')
        db.session.add(genre)
        artist.genres.append(genre)
    db.session.commit()
    db.session.close()
    flash(f"Artist {request.form['name']} was successfully listed!",'success')
    return redirect(url_for('artists'))
  else:
    flash(f"An error occurred. Artist {request.form['name']} could not be listed.",'danger')
    return render_template('forms/new_artist.html',title='New Artist', form=form)

@app.route('/artists/<artist_id>', methods=['POST'])
def delete_artist(artist_id):
  artist = Artist.query.get_or_404(artist_id)
  try:
    db.session.delete(venue)
    db.session.commit()
    flash(f'venue deleted Successfully','success')
    return redirect(url_for('index'))
  except:
    db.session.rollback()
    flash(f' error occurred on deleting artist','danger')
    return redirect(url_for('index'))
  finally:
    db.session.close() 


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  data = []
  shows = Show.query.all()
  for show in shows:
    data.append({
      "venue_id": show.Venue.id,
      "venue_name": show.Venue.name,
      "artist_id": show.Artist.id,
      "artist_name": show.Artist.name,
      "artist_image_link": show.Artist.image_link,
      "start_time": format_datetime(str(show.start_time))
    })
  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  form = ShowForm()
  return render_template('forms/new_show.html',title='New Show', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  form = ShowForm()
  if form.validate_on_submit():
    artist = Artist.query.get(form.artist_id.data)
    venue = Venue.query.get(form.venue_id.data)
    if artists and venue:
      flash(f"Show was successfully listed!",'success')
      show = Show(
        artist_id= artist.id,
        venue_id= venue.id,
        start_time= form.start_time.data,
        created_at='now()',
        updated_at='now()'
      )
      db.session.add(show)
      db.session.commit()
      db.session.close()
      return redirect(url_for('shows'))
    else:
      flash(f"please pick artist and venue are exist.",'danger')
      return redirect(url_for('create_shows'))
  else:
    flash(f"An error occurred. Show {request.form['name']} could not be listed.",'danger')
    return render_template('forms/new_show',title='New Show', form=form)

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500

