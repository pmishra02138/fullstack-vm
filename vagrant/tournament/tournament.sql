-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

CREATE DATABASE tournament;

CREATE TABLE players ( name TEXT,
                       id SERIAL PRIMARY KEY
                     );

-- What is the impact of SERIAL ID to INTEGER ID
CREATE TABLE record ( id SERIAL REFERENCES players(id),
                      wins INTEGER,
                      matches INTEGER
                    );
