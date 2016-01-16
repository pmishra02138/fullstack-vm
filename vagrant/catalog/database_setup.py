from sqlalchemy import Column, ForeignKey, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'id': self.id,
        }



class Movie(Base):
    __tablename__ = 'movie'

    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    description = Column(String(250))
    releaseDate = Column(Date)
    category_id = Column(Integer, ForeignKey('category.id'))
    movie = relationship(Category)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'releaseDate': str(self.releaseDate),
            'description': self.description,
            'id': self.id,
        }


engine = create_engine('sqlite:///moviecatalog.db')


Base.metadata.create_all(engine)
