## Movie Catalog Web App

This web application provides a catalog of movies categorized according to
different movie genres. Authorized users can create a new movie under any genre.
Users can edit or delete movies they have created.

User authentication is provided through Google OAuth2. Local permissions are
maintained to allow limited access to authorized users.

## Getting Started
* Clone a copy of [full-nanodegree-vm-repository](https://github.com/pmishra02138/fullstack-nanodegree-vm.git) to your local machine. More about file structure ca be found [here.](#fileStructure)

* Start an instance of [vagrant and virtual machine](https://www.udacity.com/wiki/ud197/install-vagrant) and go to the _synched folder_.

  ```
  vagrant up
  vagrant ssh
  cd /vagrant/catalog
  ```
* Create and populate a database
```
  python database_setup.py
  python populatecatalog.py
```

* Start catalog web app through locslhost webserver:
  ```
    python project.py
  ```
This will start a webserver on localhost at port 8000.

## Accessing web app

* To access homepage that displays all categories with the latest listed items
  ```
  localhost:8000/
  localhost:8000/categories
  ```
* Specific category with all the available items can be navigated by clicking different
links.
* New, Edit and Delete buttons are only available user has logged in through their Gmail account.
* Please **note** that CRUD is only implemented for movies.

## JSON endpoints

* Complete database can be accessed through ``` /categories/JSON```
* A particular category (genre) can be accessed through ```/category/<int:category_id>/movie/JSON```
* Detail of particlar movie can be accessed through ``` /category/<int:category_id>/movie/<int:movie_id>/JSON```

## <a id="fileStructure">File structure </a>

* The code for Movie Catalog is in /vagrant/catalog folder. The folder contains
following files:
  * **static**: This **folder** contains css stylesheet.
  * **templates**: This **folder** HTML templates corresponding to different routes.
  * **client_secrets.json**: Client secrets for authorization through Google OAuth2.
  * **database_setup.py**: File for creating an initial database.
  * **pupulatecatalog.pu**: File of populating the database.
  * **project.py**: This file contains server side code for launching the web
  app. This file contains the code for handling routes.          
