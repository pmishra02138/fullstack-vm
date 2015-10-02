#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2

def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    try:
        db = psycopg2.connect("dbname=tournament")
    except:
        print "I am unable to connect"
    return db


def deleteMatches():
    """Remove all the match records from the database."""
    db = connect()
    c = db.cursor()
    c.execute("DELETE FROM record")
    db.commit()
    db.close()


def deletePlayers():
    """Remove all the player records from the database."""
    db = connect()
    c = db.cursor()
    c.execute("DELETE FROM record")    
    c.execute("DELETE FROM players")
    db.commit()
    db.close()


def countPlayers():
    """Returns the number of players currently registered."""
    db = connect()
    c = db.cursor()
    c.execute("SELECT COUNT(*) FROM players")
    count = c.fetchall()
    db.close()

    return count[0][0]

def registerPlayer(pname):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    db = connect()
    c = db.cursor()
    c.execute("INSERT INTO players (name) VALUES (%s)", (pname,))
    c.execute("SELECT id FROM players WHERE name LIKE (%s)", (pname,))
    id_num = c.fetchall()
    c.execute("INSERT INTO record VALUES (%s, %s, %s)", (id_num[0][0], 0, 0,))
    db.commit()
    db.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    db = connect()
    c = db.cursor()
    c.execute("SELECT (players.id, players.name, record.wins, record.matches) \
                    FROM players, record WHERE players.id = record.id  \
                    ORDER BY wins DESC;")
    standings = c.fetchall()
    db.close()

    # Process output to a list of tuple form
    output = []
    for standing in standings:
        s = standing[0][1:-1].split(",")
        s[0] = int(s[0])
        s[1] = s[1][1:-1]
        s[2] = int(s[2])
        s[3] = int(s[3])
        output.append(tuple(s))

    return output


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    db = connect()
    c = db.cursor()

    c.execute("UPDATE record SET wins = wins +1, matches = matches+1 \
                WHERE id=%s", (winner,))
    c.execute("UPDATE record SET matches = matches+1 WHERE id=%s", (loser,))
    db.commit()
    db.close()


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    # Current standings of the players
    s = playerStandings()
    count = countPlayers()
    pair = []
    jmp = 0
    for i in range(0, count/2):
        pair.append(tuple([s[i+jmp][0], s[i+jmp][1], s[i+1+jmp][0], s[i+1+jmp][1]]))
        jmp = jmp + 1

    return pair
