from flask import Flask, render_template, url_for, request, redirect, jsonify, flash
import datetime

from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Movie, User

# New imports for google authentication process
from flask import session as login_session
import random
import string

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

app = Flask(__name__)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Movie Catalog Application"

# Connect to Database and create database session
engine = create_engine('sqlite:///moviecatalogwithusers.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# Create anti-forgery state token
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    return render_template('login.html', STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['credentials'] = credentials.to_json() # without to_jason() throws not JSON serilzable error
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    # See if a user exists, if it doesn't make a new one
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output


# User Helper Functions

def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session['email'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


# DISCONNECT - Revoke a current user's token and reset their login_session
@app.route('/gdisconnect')
def gdisconnect():
        # Only disconnect a connected user.
    credentials = login_session.get('credentials')

    if credentials is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # access_token = credentials.access_token
    access_token = json.loads(credentials)['access_token']
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]

    if result['status'] == '200':
        # Reset the user's sesson.
        del login_session['credentials']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']

        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        # For whatever reason, the given token was invalid.
        response = make_response(
            json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


# JSON APIs to view movie category information
@app.route('/categories/JSON')
def categoriesJSON():
    categories = session.query(Category).all()
    catalog = []
    singleCategory = {}
    for c in categories:
        singleCategory = c.serialize
        items = session.query(Movie).filter_by(category_id=c.id).all()
        singleCategory["movies"] = [i.serialize for i in items]
        catalog.append(singleCategory)

    return jsonify(categories=catalog)


@app.route('/category/<int:category_id>/movie/<int:movie_id>/JSON')
def movieItemJSON(category_id, movie_id):
    Movie_Item = session.query(Movie).filter_by(id=movie_id).one()
    return jsonify(Movie_Item=Movie_Item.serialize)

@app.route('/category/<int:category_id>/movie/JSON')
def categoryMoviesJSON(category_id):
    items = session.query(Movie).filter_by(category_id=category_id).all()
    return jsonify(MovieItems=[i.serialize for i in items])


@app.route('/')
@app.route('/categories')
def showCategories():
    categories = session.query(Category).all()
    movies =  session.query(Movie).order_by(desc(Movie.releaseDate)).limit(5).all()

    return render_template('categories.html', categories=categories, movies=movies)


@app.route('/category/<int:category_id>/movies')
def showCategory(category_id):
    categories = session.query(Category).all()
    movies =  session.query(Movie).filter(Movie.category_id == category_id).all()
    category = session.query(Category).filter(Category.id == category_id).one()
    return render_template('category.html', categories=categories,
                            movies=movies, thisCategory= category)


@app.route('/category/<int:category_id>/movie/new', methods=['GET', 'POST'])
def newMovie(category_id):
    if 'username' not in login_session:
        return redirect('/login')
    categories = session.query(Category).all()
    if request.method == 'POST':
        dt = request.form['releaseDate']
        newMovie = Movie(name = request.form['name'], releaseDate = datetime.datetime.strptime(dt, "%Y-%m-%d"),
    						description = request.form['description'], category_id = category_id, user_id=login_session['user_id'])
        session.add(newMovie)
        session.commit()
        movies =  session.query(Movie).filter(Movie.category_id == category_id).all()
        return redirect(url_for('showCategory', category_id=category_id))
    else:
        return render_template('newmovie.html', category_id=category_id)


@app.route('/category/<int:category_id>/movie/<int:movie_id>/edit', methods=['GET', 'POST'])
def editMovie(category_id, movie_id):
    if 'username' not in login_session:
        return redirect('/login')
    categories = session.query(Category).all()
    editedMovie = session.query(Movie).filter(Movie.id == movie_id).one()
    if login_session['user_id'] != editedMovie.user_id:
        return "<script>function myFunction() {alert('You are not authorized to edit this movie. You can only edit movie that you have created.');}</script><body onload='myFunction()''>"

    if request.method == 'POST':
        if request.form['name']:
            editedMovie.name = request.form['name']
        if request.form['releaseDate']:
            editedMovie.releaseDate = datetime.datetime.strptime(request.form['releaseDate'], "%Y-%m-%d")
        if request.form['description']:
            editedMovie.description = request.form['description']
        session.add(editedMovie)
        session.commit()
        return redirect(url_for('showCategory', category_id=category_id))
    else:
        return render_template('editmovie.html', category_id = category_id,
                                movie_id = movie_id, movie = editedMovie)


@app.route('/category/<int:category_id>/movie/<int:movie_id>/delete', methods=['GET', 'POST'])
def deleteMovie(category_id, movie_id):
    if 'username' not in login_session:
        return redirect('/login')
    deletedMovie = session.query(Movie).filter(Movie.id == movie_id).one()
    if login_session['user_id'] != deletedMovie.user_id:
        return "<script>function myFunction() {alert('You are not authorized to delete this movie. You can only delete movie that you have created.');}</script><body onload='myFunction()''>"

    if request.method == 'POST':
        session.delete(deletedMovie)
        session.commit()
        return redirect(url_for('showCategory', category_id=category_id))
    else:
        return render_template('deletemovie.html', category_id = category_id,
                                movie_id = movie_id, movie = deletedMovie)


@app.route('/category/<int:category_id>/movie/<int:movie_id>')
def showMovie(category_id, movie_id):
    movie =  session.query(Movie).filter(Movie.category_id == category_id, Movie.id == movie_id).one()
    creator = getUserInfo(movie.user_id)
    if 'username' not in login_session or creator.id != login_session['user_id']:
        return render_template('publicshowmovie.html', movie = movie)
    else:
        return render_template('showmovie.html', movie = movie)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
