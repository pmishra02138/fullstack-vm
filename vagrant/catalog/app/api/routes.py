from flask import jsonify


# JSON APIs to view movie category information
@api.route('/categories/JSON')
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


@api.route('/category/<int:category_id>/movie/<int:movie_id>/JSON')
def movieItemJSON(category_id, movie_id):
    Movie_Item = session.query(Movie).filter_by(id=movie_id).one()
    return jsonify(Movie_Item=Movie_Item.serialize)


@app.route('/category/<int:category_id>/movie/JSON')
def categoryMoviesJSON(category_id):
    items = session.query(Movie).filter_by(category_id=category_id).all()
    return jsonify(MovieItems=[i.serialize for i in items])
