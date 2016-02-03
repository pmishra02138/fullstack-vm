# from sqlalchemy import Column, ForeignKey, Integer, String, Date
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import relationship
# from sqlalchemy import create_engine
from . import db


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(250), nullable=False)


class Category(db.Model):
    __tablename__ = 'category'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'id': self.id,
        }


class Movie(db.Model):
    __tablename__ = 'movie'

    name = db.Column(db.String(80), nullable=False)
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(250))
    releaseDate = db.Column(db.Date)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    movie = db.relationship(Category)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship(User)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'releaseDate': str(self.releaseDate),
            'description': self.description,
            'id': self.id,
        }

# Uncomment following to create the database

# db.create_all()
