from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Base, Category, Movie, User
from random import randint
import datetime
import random


engine = create_engine('sqlite:///moviecatalogwithusers.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

# Create Users
# User1
newUser = User(name = "Pankaj Mishra", email="pmishra02138@gmail.com")
session.add(newUser)
session.commit()

# User2
newUser = User(name = "Pankaj", email="pankaj501@hotmail.com")
session.add(newUser)
session.commit()

# Print Users
# for user in session.query(User):
# 	print user.name, user.id, user.email

# Add Categories
categories = ['Action', 'Comedies', 'Dramas', 'Romance', 'Horror']

for i, category in enumerate(categories):
	new_category = Category(name = category)
	session.add(new_category)
	session.commit()

# Print Catalog table
# for category in session.query(Category):
# 	print category.name, category.id

# Add movies
movies = [{'name':'Surviovr', 'category':'Action', 'releaseDate':datetime.date(2015, 5, 29),'description': 'A Foreign Service Officer in London tries to prevent a terrorist attack set to hit New York, but is forced to go on the run when she is framed for crimes she did not commit.'},
			{'name':'Swordfish', 'category':'Action', 'releaseDate':datetime.date(2001, 6, 8), 'description': 'Determined to get his mitts on $9 billion in a secret DEA account so he can use it to fight terrorism, rogue agent Gabriel Shear recruits encryption expert Stanley Jobson to hack into the government mainframe.'},
			{'name':'The Ridiculous 6', 'category':'Comedies', 'releaseDate':datetime.date(2015,12, 11), 'description':'An outlaw who was raised by Native Americans discovers that he has five half-brothers; together the men go on a mission to find their wayward, deadbeat dad.'},
			{'name':'Along Came Polly', 'category':'Comedies', 'releaseDate': datetime.date(2004, 1,16), 'description':'A buttoned up newlywed finds his too organized life falling into chaos when he falls in love with an old classmate.'},
			{'name':'Big Sky', 'category':'Dramas','releaseDate':datetime.date(2015, 8, 14), 'description':'Suffering from paralyzing agoraphobia, teenage Hazel is headed to a treatment center with her mother when two brothers attack them along the way. With her mom wounded, Hazel is forced to battle the men -- and her fears -- in a struggle to survive.'},
			{'name':'Uncanny', 'category':'Dramas','releaseDate':datetime.date(2015, 1, 31), 'description':'A journalist visits an inventor who\'s made a groundbreaking leap in his work with humanoid robots. But his creation proves to be all too lifelike.'},
			{'name':'Slow Learners', 'category':'Romance', 'releaseDate':datetime.date(2015, 4, 20), 'description':'When platonic pals (and colleagues) Jeff Lowry and Anne Martin fail to ignite sparks in their romantic lives, they make a pact to "improve" themselves, launching a makeover campaign they\'re certain will leave them confident and lucky in love.'},
			{'name':'Something New', 'category':'Romance','releaseDate':datetime.date(2006, 1, 29), 'description':'Struggling with her personal life, black career woman Kenya agrees to a blind date with a sexy, free-spirited landscape architect. Her new love interest is white, which isn\'t necessarily a deal-breaker, until she meets a seemingly perfect black man.'},
			{'name':'Pay the Ghost', 'category':'Horror','releaseDate':datetime.date(2015, 9, 25), 'description':'Nearly a year after his 8-year-old son vanishes in the midst of a Halloween parade, Mike Cole begins having horrifying visions of the boy\'s fate. Renewing his search for the youngster, Mike realizes he\'s up against a vengeful Halloween spirit.'},
			{'name':'Awaken', 'category':'Horror', 'releaseDate':datetime.date(2015, 7, 7), 'description':'A random group of people played by Vinnie Jones, Edward Furlong, and Daryl Hannah amongst others wake up on an Island where they are being hunted down in a sinister plot to harvest their organs.'}]

for i, movie in enumerate(movies):
	movieCategory = session.query(Category).filter(Category.name== movie['category']).one()
	new_movie = Movie(name = movie['name'], releaseDate = movie['releaseDate'],
						description = movie['description'], category_id = movieCategory.id, user_id=randint(1,2))
	session.add(new_movie)
	session.commit()

# Print Movie table
# for movie in session.query(Movie):
# 	print movie.name, movie.id, movie.category_id, movie.user_id, movie.releaseDate, movie.description

print "Successfully created Catalog database containing movies by generes!"
