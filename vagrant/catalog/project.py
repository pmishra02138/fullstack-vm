from flask import Flask, render_template, url_for, request, redirect, jsonify
import datetime

from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Movie

# New imports for google authentication process
from flask import session as login_session
import random
import string


app = Flask(__name__)


# Connect to Database and create database session
engine = create_engine('sqlite:///moviecatalog.db')
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
def restaurantMenuJSON(category_id):
    items = session.query(Movie).filter_by(category_id=category_id).all()
    return jsonify(MovieItems=[i.serialize for i in items])


@app.route('/')
@app.route('/categories')
def showCategories():
    categories = session.query(Category).all()
    movies =  session.query(Movie).order_by(asc(Movie.releaseDate)).limit(5).all()
    return render_template('categories.html', categories=categories, movies=movies)


@app.route('/category/<int:category_id>/movies')
def showCategory(category_id):
    categories = session.query(Category).all()
    movies =  session.query(Movie).filter(Movie.category_id == category_id).all()
    return render_template('category.html', categories=categories,
                            category_id = category_id, movies=movies)


@app.route('/category/<int:category_id>/movie/new', methods=['GET', 'POST'])
def newMovie(category_id):
    categories = session.query(Category).all()
    if request.method == 'POST':
        dt = request.form['releaseDate']
        newMovie = Movie(name = request.form['name'], releaseDate = datetime.datetime.strptime(dt, "%Y-%m-%d"),
    						description = request.form['description'], category_id = category_id)
        session.add(newMovie)
        session.commit()
        movies =  session.query(Movie).filter(Movie.category_id == category_id).all()
        return redirect(url_for('showCategory', category_id=category_id))
    else:
        return render_template('newmovie.html', category_id=category_id)


@app.route('/category/<int:category_id>/movie/<int:movie_id>/edit', methods=['GET', 'POST'])
def editMovie(category_id, movie_id):
    categories = session.query(Category).all()
    editedMovie = session.query(Movie).filter(Movie.id == movie_id).one()
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
    deletedMovie = session.query(Movie).filter(Movie.id == movie_id).one()
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
    return render_template('showmovie.html', movie = movie)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
