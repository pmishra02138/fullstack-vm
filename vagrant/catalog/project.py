from flask import Flask
app = Flask(__name__)


@app.route('/')
@app.route('/categories')
def showCategories():
    return "This page will show all movie categories."


@app.route('/category/<int:category_id>/movies')
def showCategory(category_id):
    return "This page will show all movies in category: %d " % (category_id, )


@app.route('/category/<int:category_id>/movie/new')
def newMovie(category_id):
    return "This page will create a new movie in category: %d" % (category_id, )


@app.route('/category/<int:category_id>/movie/<int:movie_id>/edit')
def editMovie(category_id, movie_id):
    return "This page will edit movie: %d in category: %d" % (movie_id, category_id)


@app.route('/category/<int:category_id>/movie/<int:movie_id>/delete')
def deleteMovie(category_id, movie_id):
    return "This page will delete movie: %d in category: %d" % (movie_id, category_id)


@app.route('/category/<int:category_id>/movie/<int:movie_id>')
def showMovie(category_id, movie_id):
    return "This page will show descritption of movie: %d in category: %d" % (movie_id, category_id)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
