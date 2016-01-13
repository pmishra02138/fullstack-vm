from flask import Flask, render_template, url_for, request


from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Movie


app = Flask(__name__)


# Connect to Database and create database session
engine = create_engine('sqlite:///moviecatalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


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
    if request.method == 'POST':
        pass
    else:
        return render_template('newmovie.html', category_id=category_id)


@app.route('/category/<int:category_id>/movie/<int:movie_id>/edit', methods=['GET', 'POST'])
def editMovie(category_id, movie_id):
    editedMovie = session.query(Movie).filter(Movie.id == movie_id).one()
    if request.method == 'POST':
        pass
    else:
        return render_template('editmovie.html', category_id = category_id,
                                movie_id = movie_id, movie = editedMovie)


@app.route('/category/<int:category_id>/movie/<int:movie_id>/delete', methods=['GET', 'POST'])
def deleteMovie(category_id, movie_id):
    deletedMovie = session.query(Movie).filter(Movie.id == movie_id).one()
    if request.method == 'POST':
        pass
    else:
        return render_template('deletemovie.html', category_id = category_id,
                                movie_id = movie_id, movie = deletedMovie)


@app.route('/category/<int:category_id>/movie/<int:movie_id>', methods=['GET', 'POST'])
def showMovie(category_id, movie_id):
    movie =  session.query(Movie).filter(Movie.category_id == category_id, Movie.id == movie_id).one()
    if request.method == 'POST':
        pass
    else:
        return render_template('showmovie.html', movie = movie)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
