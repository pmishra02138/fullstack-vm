## Tournament Results

Tournament Results project comprises a database to keep track of players and matches in a Swiss Pairing based game tournament.  Database schema definition is in tournament .sql and the code to keep track of swiss tournament is in tournament.py

## Getting Started
* First, clone a copy of [full-nanodegree-vm-repository](https://github.com/pmishra02138/fullstack-nanodegree-vm.git) to your local machine.

* The code for Tournament Results is in /vagrant/tournament folder. This folder contains following files:
   * **tournament.sql**: This file creates a database database containing two tables. First table contains player info and the second one contains their match record. This databases can be queried to to determine the winners of various games and players standings based on swiss pairing system.

   * **tournament.py**: This file provides access to the database via library functions.

   * **tournament_test.py**: This file contains a series of functions to test the implementation of various of functions in tournament.py

## Using vagrant and virtual machine

* The vagrant VM has PostgresSQL installed and configured and it also has command line interface (CLI).

* Navigate to the /vagrant/tournament folder and type ```vagrant up``` followed by ```vagrant ssh```. After this go to _synched folder_ by typing ```cd /vagrant```

Note:  Help with installaing vagrant and virual box can be found [here.](https://www.udacity.com/wiki/ud197/install-vagrant)

## Using the psql command line interface

* To build and access the database please run ```psql``` followed by ```\i tournament.sql```

* Here are other useful psql commands:

|command | Description|Usage|
|--------|------------|-----|
|psql| launch the psql CLI | psql tournament|
|\c connect|connect to the database|\c tournament |
|\i | execute sql commands from a file|\i tournament.psql|
|\q | quit| \q |
|\?|help| \?|

## Downloading
There are two ways this software can be accessed. These are as follows:

**Git Access**
The latest version of code can be directly cloned from[full-nanodegree-vm-repository.](https://github.com/pmishra02138/fullstack-nanodegree-vm.git)
Code for Tournament Results is in ```/vagrant/tournament``` folder.

**Zip download**
A zip version of Tournament Results can be downloaded from [here.](https://github.com/pmishra02138/fullstack-nanodegree-vm/archive/master.zip)

## Bug Reporting

Please file a pull request for bug reporting.

## System-specific Notes

The code is tested on 32 -bit ubunutu 14.04.2 LTS hosted on vagrant and virtualbox in a windows machine.
