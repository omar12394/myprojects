#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import (
Flask,
render_template,
request,
Response,
flash,
redirect,
url_for)
from flask_moment import Moment
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from sqlalchemy import func
from forms import *
from models import (
  app,
  db,
  Venue,
  Artist,
  Shows
)
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

moment = Moment(app)
app.config.from_object('config')
# TODO: connect to a local postgresql database

#work area 1  not done

#end work area 1


db.create_all()

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
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  q=Venue.query.order_by(db.desc(Venue.id)).limit(3).all()

  data=list(map(lambda x:{
    "city": x.city,
    "state":x.state,
    "venues":list(map(lambda y:{
      "id": y.id,
      "name": y.name,
      "num_upcoming_shows": len(Shows.query.filter(Shows.start_time > datetime.utcnow(), Shows.venue_id == y.id).all())
      },Venue.query.filter_by(city=x.city,state=x.state).limit(3).all()))},q))
  return render_template('pages/venues.html', areas=data)

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  q = Venue.query.filter(func.lower(Venue.name).like('%'+request.form.get('search_term').lower()+'%')).all()
  response={
    "count": len(q),
    "data":list(map(lambda x:{
      "id": x.id,
      "name": x.name,
      "num_upcoming_shows":Shows.query.filter(Shows.start_time > datetime.utcnow(), Shows.venue_id ==  x.id).all()
    },q))
  }
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  #region[]
  # data1={
  #   "id": 1,
  #   "name": "The Musical Hop",
  #   "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
  #   "address": "1015 Folsom Street",
  #   "city": "San Francisco",
  #   "state": "CA",
  #   "phone": "123-123-1234",
  #   "website": "https://www.themusicalhop.com",
  #   "facebook_link": "https://www.facebook.com/TheMusicalHop",
  #   "seeking_talent": True,
  #   "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
  #   "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
  #   "past_shows": [{
  #     "artist_id": 4,
  #     "artist_name": "Guns N Petals",
  #     "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
  #     "start_time": "2019-05-21T21:30:00.000Z"
  #   }],
  #   "upcoming_shows": [],
  #   "past_shows_count": 1,
  #   "upcoming_shows_count": 0,
  # }
  # data2={
  #   "id": 2,
  #   "name": "The Dueling Pianos Bar",
  #   "genres": ["Classical", "R&B", "Hip-Hop"],
  #   "address": "335 Delancey Street",
  #   "city": "New York",
  #   "state": "NY",
  #   "phone": "914-003-1132",
  #   "website": "https://www.theduelingpianos.com",
  #   "facebook_link": "https://www.facebook.com/theduelingpianos",
  #   "seeking_talent": False,
  #   "image_link": "https://images.unsplash.com/photo-1497032205916-ac775f0649ae?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=750&q=80",
  #   "past_shows": [],
  #   "upcoming_shows": [],
  #   "past_shows_count": 0,
  #   "upcoming_shows_count": 0,
  # }
  # data3={
  #   "id": 3,
  #   "name": "Park Square Live Music & Coffee",
  #   "genres": ["Rock n Roll", "Jazz", "Classical", "Folk"],
  #   "address": "34 Whiskey Moore Ave",
  #   "city": "San Francisco",
  #   "state": "CA",
  #   "phone": "415-000-1234",
  #   "website": "https://www.parksquarelivemusicandcoffee.com",
  #   "facebook_link": "https://www.facebook.com/ParkSquareLiveMusicAndCoffee",
  #   "seeking_talent": False,
  #   "image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
  #   "past_shows": [{
  #     "artist_id": 5,
  #     "artist_name": "Matt Quevedo",
  #     "artist_image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
  #     "start_time": "2019-06-15T23:00:00.000Z"
  #   }],
  #   "upcoming_shows": [{
  #     "artist_id": 6,
  #     "artist_name": "The Wild Sax Band",
  #     "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
  #     "start_time": "2035-04-01T20:00:00.000Z"
  #   }, {
  #     "artist_id": 6,
  #     "artist_name": "The Wild Sax Band",
  #     "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
  #     "start_time": "2035-04-08T20:00:00.000Z"
  #   }, {
  #     "artist_id": 6,
  #     "artist_name": "The Wild Sax Band",
  #     "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
  #     "start_time": "2035-04-15T20:00:00.000Z"
  #   }],
  #   "past_shows_count": 1,
  #   "upcoming_shows_count": 1,
  # }
  #endregion[]
  vn = Venue.query.get(venue_id)
  # ps = Shows.query.filter(Shows.start_time<datetime.utcnow(),Shows.venue_id==venue_id).all()
  # cs = Shows.query.filter(Shows.start_time>datetime.utcnow(),Shows.venue_id==venue_id).all()
  
  #using join 
  ps= db.session.query(Shows).join(Artist).filter(Shows.venue_id==venue_id,Shows.start_time<datetime.utcnow()).all() #past shows
  cs= db.session.query(Shows).join(Artist).filter(Shows.venue_id==venue_id,Shows.start_time>datetime.utcnow()).all() #upcoming shows

  # data0 = list(filter(lambda d: d['id'] == venue_id, [data1, data2, data3]))[0]
  print('\n\n ps is ::: \n\n',ps)
  
  data={
    "id": vn.id,
    "name": vn.name,
    "genres": vn.genres,
    "address": vn.address,
    "city": vn.city,
    "state":vn.state,
    "phone": vn.phone,
    "website":vn.website,
    "facebook_link":vn.facebook_link,
    "seeking_talent": vn.seeking_talent,
    'seeking_description':vn.seeking_description,
    "image_link": vn.image_link,
    "past_shows":list(map(lambda x:{
      "artist_id": x.artist_id,
      "artist_name":Artist.query.get(x.artist_id).name,
      "artist_image_link":Artist.query.get(x.artist_id).image_link,
      "start_time": x.start_time.strftime('%Y-%m-%d %H:%M:%S')
    },ps)),
    "upcoming_shows":list(map(lambda x:{
      "artist_id": x.artist_id,
      "artist_name":Artist.query.get(x.artist_id).name,
      "artist_image_link":Artist.query.get(x.artist_id).image_link,
      "start_time": x.start_time.strftime('%Y-%m-%d %H:%M:%S')
    },cs)),
    "past_shows_count": len(ps),
    "upcoming_shows_count": len(cs),
  }
  try:
   return render_template('pages/show_venue.html', venue=data)
  except TypeError:
    return render_template('errors/404.html')
    


#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  
  rl_data=Venue()
  for i in request.form.keys():
    if i != 'seeking_talent':
      setattr(rl_data, i, request.form.get(i))
      print('\n', i, ' ', request.form.get(i))
    else:
      if 'y' == request.form.get(i):
        setattr(rl_data, i,True)
      else:
        setattr(rl_data, i, False)




  try:
    db.session.add(rl_data)
    db.session.commit()
    flash('Venue ' + request.form['name'] + ' was successfully listed!')

  except:
    flash('An error occured. venue ' + request.form['name'] + '  could not be listed.')


  # on successful db insert, flash success
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')
@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
  q = Venue.query.get(venue_id)
  db.session.remove(q)
  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return None

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database
  q=Artist.query.limit(3).all()

  data=list(map(lambda x:{
    "id": x.id,
    "name": x.name,
 
  },q))
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  
  q = Artist.query.filter(func.lower(Artist.name).like('%'+request.form.get('search_term').lower()+'%')).all()
  response={
    "count": len(q),
    "data":list(map(lambda x:{
      "id": x.id,
      "name": x.name,
      "num_upcoming_shows":Shows.query.filter(Shows.start_time > datetime.utcnow(), Shows.artist_id ==  x.id).all()
    },q))
  }
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  #region[]
  # data1={
  #   "id": 4,
  #   "name": "Guns N Petals",
  #   "genres": ["Rock n Roll"],
  #   "city": "San Francisco",
  #   "state": "CA",
  #   "phone": "326-123-5000",
  #   "website": "https://www.gunsnpetalsband.com",
  #   "facebook_link": "https://www.facebook.com/GunsNPetals",
  #   "seeking_venue": True,
  #   "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
  #   "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
  #   "past_shows": [{
  #     "venue_id": 1,
  #     "venue_name": "The Musical Hop",
  #     "venue_image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
  #     "start_time": "2019-05-21T21:30:00.000Z"
  #   }],
  #   "upcoming_shows": [],
  #   "past_shows_count": 1,
  #   "upcoming_shows_count": 0,
  # }
  # data2={
  #   "id": 5,
  #   "name": "Matt Quevedo",
  #   "genres": ["Jazz"],
  #   "city": "New York",
  #   "state": "NY",
  #   "phone": "300-400-5000",
  #   "facebook_link": "https://www.facebook.com/mattquevedo923251523",
  #   "seeking_venue": False,
  #   "image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
  #   "past_shows": [{
  #     "venue_id": 3,
  #     "venue_name": "Park Square Live Music & Coffee",
  #     "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
  #     "start_time": "2019-06-15T23:00:00.000Z"
  #   }],
  #   "upcoming_shows": [],
  #   "past_shows_count": 1,
  #   "upcoming_shows_count": 0,
  # }
  # data3={
  #   "id": 6,
  #   "name": "The Wild Sax Band",
  #   "genres": ["Jazz", "Classical"],
  #   "city": "San Francisco",
  #   "state": "CA",
  #   "phone": "432-325-5432",
  #   "seeking_venue": False,
  #   "image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
  #   "past_shows": [],
  #   "upcoming_shows": [{
  #     "venue_id": 3,
  #     "venue_name": "Park Square Live Music & Coffee",
  #     "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
  #     "start_time": "2035-04-01T20:00:00.000Z"
  #   }, {
  #     "venue_id": 3,
  #     "venue_name": "Park Square Live Music & Coffee",
  #     "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
  #     "start_time": "2035-04-08T20:00:00.000Z"
  #   }, {
  #     "venue_id": 3,
  #     "venue_name": "Park Square Live Music & Coffee",
  #     "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
  #     "start_time": "2035-04-15T20:00:00.000Z"
  #   }],
  #   "past_shows_count": 0,
  #   "upcoming_shows_count": 3,
  # }
  # data0 = list(filter(lambda d: d['id'] == artist_id, [data1, data2, data3]))[0]
  #endregion[]
  vn = Artist.query.get(artist_id)
  # ps = Shows.query.filter(Shows.start_time < datetime.utcnow(), Shows.artist_id == artist_id).all()
  # cs = Shows.query.filter(Shows.start_time > datetime.utcnow(), Shows.artist_id == artist_id).all()
  
  #using join 
  ps= db.session.query(Shows).join(Venue).filter(Shows.artist_id==artist_id,Shows.start_time<datetime.utcnow()).all() #past shows
  cs= db.session.query(Shows).join(Venue).filter(Shows.artist_id==artist_id,Shows.start_time>datetime.utcnow()).all() #upcoming shows


  data={
    "id": vn.id,
    "name": vn.name,
    "genres": vn.genres,
    "city": vn.city,
    "state":vn.state,
    "phone": vn.phone,
    "website":vn.website,
    "facebook_link":vn.facebook_link,
    "seeking_venue": vn.seeking_venue,
    'seeking_description':vn.seeking_description,
    "image_link": vn.image_link,
    "past_shows":list(map(lambda x:{
      "venue_id": x.venue_id,
      "venue_name":Venue.query.get(x.venue_id).name,
      "venue_image_link":Venue.query.get(x.venue_id).image_link,
      "start_time": x.start_time.strftime('%Y-%m-%d %H:%M:%S')
    },ps)),
    "upcoming_shows": list(map(lambda x:{
      "venue_id": x.venue_id,
      "venue_name":Venue.query.get(x.venue_id).name,
      "venue_image_link":Venue.query.get(x.venue_id).image_link,
      "start_time": x.start_time.strftime('%Y-%m-%d %H:%M:%S')
    },cs)),
    "past_shows_count": len(ps),
    "upcoming_shows_count": len(cs),
  }

  try:
    return render_template('pages/show_artist.html', artist=data)
  except TypeError:
    print(vn)
    return render_template('errors/404.html')
    

  
  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  vn = Artist.query.get(artist_id)
  artist={
    "id": vn.id,
    "name": vn.name,
    "genres": vn.genres,
    "city": vn.city,
    "state":vn.state,
    "phone": vn.phone,
    "website":vn.website,
    "facebook_link":vn.facebook_link,
    "seeking_venue": vn.seeking_venue,
    'seeking_description':vn.seeking_description,
    "image_link": vn.image_link

  }
  # TODO: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
  rl_data=Artist().query.get(artist_id)
  setattr(rl_data, 'seeking_venue', False)
  for i in request.form.keys():
    if i != 'seeking_venue':
      setattr(rl_data, i, request.form.get(i))
      print('\n', i, ' ', request.form.get(i))
    else:
      if 'y' == request.form.get(i):
        setattr(rl_data, i,True)
      else:
        setattr(rl_data, i, False)
    
  try:
    db.session.commit()
  except:
    flash('An error occured. venue ' + request.form['name'] + '  could not be listed.')
  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  vn = Venue.query.get(venue_id)
  venue={
    "id": vn.id,
    "name": vn.name,
    "genres": vn.genres,
    "address": vn.address,
    "city": vn.city,
    "state":vn.state,
    "phone": vn.phone,
    "website":vn.website,
    "facebook_link":vn.facebook_link,
    "seeking_talent": vn.seeking_talent,
    'seeking_description':vn.seeking_description,
    "image_link": vn.image_link
    }
  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  rl_data = Venue().query.get(venue_id)
  setattr(rl_data, 'seeking_talent', False)

  for i in request.form.keys():
    if i != 'seeking_talent':
      setattr(rl_data, i, request.form.get(i))
      print('\n', i, ' ', request.form.get(i))
    else:
      if 'y' == request.form.get(i):
        setattr(rl_data, i,True)
      else:
        setattr(rl_data, i, False)
  try:
    db.session.commit()
  except:
    flash('An error occured. venue ' + request.form['name'] + '  could not be listed.')
  # venue record with ID <venue_id> using the new attributes
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  rl_data=Artist()
  exdname=['name','city','state','genres','address','phone','state','image_link','website','facebook_link','seeking_venue','seeking_description']

  for i in  request.form.keys():
    if i != 'seeking_venue':
      setattr(rl_data, i, request.form.get(i))
      print('\n', i, ' ', request.form.get(i))
    else:
      if 'y' == request.form.get(i):
        setattr(rl_data, i,True)
      else:
        setattr(rl_data, i, False)


  try:
    db.session.add(rl_data)
    db.session.commit()
    flash('Artist ' + request.form['name'] + ' was successfully listed!')

  except:
    flash('An error occured. Artist ' + request.form['name'] + '  could not be listed.')

  # on successful db insert, flash success
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  q=Shows.query.all()
  data=list(map(lambda x:{
    "venue_id":  Venue.query.get(x.venue_id).id,
    "venue_name": Venue.query.get(x.venue_id).name,
    "artist_id":  Artist.query.get(x.venue_id).id,
    "artist_name": Artist.query.get(x.artist_id).name,
    "artist_image_link":  Artist.query.get(x.artist_id).image_link,
    "start_time":  x.start_time.strftime('%Y-%m-%d %H:%M:%S')
  },q))
  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead

  # on successful db insert, flash success
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  rl_data=Shows()
  for i in  request.form.keys():
    setattr(rl_data, i, request.form.get(i))

  try:
    db.session.add(rl_data)
    db.session.commit()
    flash('Show '  + ' was successfully listed!')

  except:
    flash('An error occured. Show ' + '  could not be listed.')

  # on successful db insert, flash success
  return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
