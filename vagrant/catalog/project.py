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
    return render_template('categories.html', categories=categories)


@app.route('/category/<int:category_id>/movies')
def showCategory(category_id):
    categories = session.query(Category).all()
    
    return render_template('category.html', categories=categories,
                            category_id = category_id, movie = movies[category_id-1])


@app.route('/category/<int:category_id>/movie/new', methods=['GET', 'POST'])
def newMovie(category_id):
    # return "This page will create a new movie in category: %d" % (category_id, )
    if request.method == 'POST':
        pass
    else:
        return render_template('newmovie.html', category_id=category_id)


@app.route('/category/<int:category_id>/movie/<int:movie_id>/edit', methods=['GET', 'POST'])
def editMovie(category_id, movie_id):
    # return "This page will edit movie: %d in category: %d" % (movie_id, category_id)
    if request.method == 'POST':
        pass
    else:
        return render_template('editmovie.html', categories=categories,
                                category_id = category_id, movie_id = movie_id,
                                movie = movies[category_id])


@app.route('/category/<int:category_id>/movie/<int:movie_id>/delete', methods=['GET', 'POST'])
def deleteMovie(category_id, movie_id):
    # return "This page will delete movie: %d in category: %d" % (movie_id, category_id)
    if request.method == 'POST':
        pass
    else:
        return render_template('deletemovie.html', categories=categories,
                                category_id = category_id, movie_id = movie_id,
                                movie = movies[category_id])


@app.route('/category/<int:category_id>/movie/<int:movie_id>', methods=['GET', 'POST'])
def showMovie(category_id, movie_id):
    # return "This page will show descritption of movie: %d in category: %d" % (movie_id, category_id)
    if request.method == 'POST':
        pass
    else:
        return render_template('showmovie.html', category_id = category_id,
                                movie_id = movie_id, movie = movies[category_id])


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
