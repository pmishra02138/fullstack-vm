from flask import render_template, url_for, request, redirect
import datetime

from .import moviecatalog
from .. import db
from ..models import User, Category, Movie
from .forms import MovieForm


@moviecatalog.route('/')
@moviecatalog.route('/categories')
def showCategories():
    categories = Category.query.all()
    movies =  Movie.query.order_by(db.desc(Movie.releaseDate)).limit(5).all()
    return render_template('categories.html', categories=categories, movies=movies)


@moviecatalog.route('/category/<int:category_id>/movies')
def showCategory(category_id):
    categories = db.session.query(Category).all()
    movies =  db.session.query(Movie).filter(Movie.category_id == category_id).all()
    category = db.session.query(Category).filter(Category.id == category_id).one()
    return render_template('category.html', categories=categories,
                            movies=movies, thisCategory=category)

#
# @moviecatalog.route('/category/<int:category_id>/movie/new', methods=['GET', 'POST'])
# @login_required
# def newMovie(category_id):
#     categories = db.session.query(Category).all()
#     form = MovieForm()
#     if request.method == 'POST':
#         dt = request.form['releaseDate']
#         newMovie = Movie(name = request.form['name'],
#                         releaseDate = datetime.datetime.strptime(dt, "%Y-%m-%d"),
#                         description = request.form['description'],
#                         category_id = category_id, user_id=login_session['user_id'])
#         db.session.add(newMovie)
#         db.session.commit()
#         movies =  db.session.query(Movie).filter(Movie.category_id == category_id).all()
#         return redirect(url_for('showCategory', category_id=category_id))
#     else:
#         return render_template('newmovie.html', category_id=category_id,
#                                 form = form)
#
#
# @moviecatalog.route('/category/<int:category_id>/movie/<int:movie_id>/edit',
#             methods=['GET', 'POST'])
# @login_required
# def editMovie(category_id, movie_id):
#     categories = db.session.query(Category).all()
#     editedMovie = db.session.query(Movie).filter(Movie.id == movie_id).one()
#     form = MovieForm()
#     if login_session['user_id'] != editedMovie.user_id:
#         return "<script>function myFunction() {alert('You are not authorized \
#                 to edit this movie. You can only edit movie that you have \
#                 created.');}</script><body onload='myFunction()''>"
#
#     if request.method == 'POST':
#         if request.form['name']:
#             editedMovie.name = request.form['name']
#         if request.form['releaseDate']:
#             editedMovie.releaseDate = datetime.datetime.strptime(request.form['releaseDate'], "%Y-%m-%d")
#         if request.form['description']:
#             editedMovie.description = request.form['description']
#         db.session.add(editedMovie)
#         db.session.commit()
#         return redirect(url_for('showCategory', category_id=category_id))
#     else:
#         return render_template('editmovie.html', category_id = category_id,
#                                 movie_id = movie_id, movie = editedMovie,
#                                 form=form)
#
#
# @moviecatalog.route('/category/<int:category_id>/movie/<int:movie_id>/delete', methods=['GET', 'POST'])
# @login_required
# def deleteMovie(category_id, movie_id):
#     deletedMovie = db.session.query(Movie).filter(Movie.id == movie_id).one()
#     if login_session['user_id'] != deletedMovie.user_id:
#         return "<script>function myFunction() {alert('You are not authorized \
#                 to delete this movie. You can only delete movie that you have \
#                 created.');}</script><body onload='myFunction()''>"
#
#     if request.method == 'POST':
#         db.session.delete(deletedMovie)
#         db.session.commit()
#         return redirect(url_for('showCategory', category_id=category_id))
#     else:
#         return render_template('deletemovie.html', category_id = category_id,
#                                 movie_id = movie_id, movie = deletedMovie)
#
#
@moviecatalog.route('/category/<int:category_id>/movie/<int:movie_id>')
def showMovie(category_id, movie_id):
    movie =  db.session.query(Movie).filter(Movie.category_id == category_id, Movie.id == movie_id).one()
    creator = getUserInfo(movie.user_id)
    if 'username' not in login_session or creator.id != login_session['user_id']:
        return render_template('publicshowmovie.html', movie = movie)
    else:
        return render_template('showmovie.html', movie = movie)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
