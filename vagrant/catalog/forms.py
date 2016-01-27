from flask.ext.wtf import Form
from wtforms import StringField, DateField, TextAreaField

class NewMovieForm(Form):
    name = StringField('Name')
    releaseDate = DateField('ReleaseDate')
    description = TextAreaField('Synopsis')
