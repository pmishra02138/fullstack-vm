from flask.ext.wtf import Form
from wtforms import StringField, DateField, TextAreaField

class MovieForm(Form):
    name = StringField('Name')
    releaseDate = DateField('ReleaseDate')
    description = TextAreaField('Synopsis')
