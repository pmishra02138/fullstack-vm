from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from moviecatalog import Base, Category, Movie
from random import randint
import datetime
import random


engine = create_engine('sqlite:///moviecatalog.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


# Add Categories
category1 = Category(name = "Action")
session.add(category1)

category2 = Category(name = "Comedies")
session.add(category2)

category3 = Category(name = "Drama")
session.add(category3)

category4 = Category(name = "Romance")
session.add(category4)

category5 = Category(name = "Horror")
session.add(category5)


# Add movoies
