from flask import Flask, render_template, url_for, request
app = Flask(__name__)


# Fake Categories
category = {'name': 'Action', 'id': '1'}
categories = [{'name':'Action', 'id': '1'}, {'name':'Comedies', 'id': '2'}, {'name':'Drama', 'id': '3'},
 {'name':'Romance', 'id': '4'}, {'name':'Horror', 'id': '5'}]

#Fake Menu Items
movies = [ {'name':'Survivor', 'description':'made with fresh cheese', 'price':'$5.99','course' :'Entree', 'id':'1'},
{'name':'Chocolate Cake','description':'made with Dutch Chocolate', 'price':'$3.99', 'course':'Dessert','id':'2'},
{'name':'Caesar Salad', 'description':'with fresh organic vegetables','price':'$5.99', 'course':'Entree','id':'3'},
{'name':'Iced Tea', 'description':'with lemon','price':'$.99', 'course':'Beverage','id':'4'},
{'name':'Spinach Dip', 'description':'creamy dip with fresh spinach','price':'$1.99', 'course':'Appetizer','id':'5'} ]
movie =  {'name':'Surviovr','description':'A Foreign Service Officer in London tries to prevent a terrorist attack set to hit New York, but is forced to go on the run when she is framed for crimes she did not commit.'}


@app.route('/')
@app.route('/categories')
def showCategories():
    # return "This page will show all movie categories."
    return render_template('categories.html', categories=categories)


@app.route('/category/<int:category_id>/movies')
def showCategory(category_id):
    # return "This page will show all movies in category: %d " % (category_id, )
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
