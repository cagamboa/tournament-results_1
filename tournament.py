#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    try:
        db = psycopg2.connect("dbname=tournament")
        c = db.cursor()
        return db, c
    except:
        print("<Unable to connect to the database")
    return db,c


def deleteMatches():
    """Remove all the match records from the database."""
    db,c = connect()
    c.execute("DELETE from matches")    
    db.commit()
    db.close()

def deletePlayers():
    """Remove all the player records from the database."""
    db,c = connect()
    c.execute("DELETE FROM tournament")
    db.commit()
    db.close()  


def countPlayers():
    """Returns the number of players currently registered."""
    db,c = connect()
    c.execute("SELECT count(*) as num FROM tournament;")
    db.commit()
    counter = c.fetchone()[0]
    db.close()
    return counter


def registerPlayer(playername):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    
    create a player called First Player
    --Don't need to add id -- this is a serial & primary key"""
    
    db,c = connect()
    c.execute( "INSERT INTO tournament (name) VALUES(%s)", (playername,))
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
    db,c = connect() 
    c.execute("select * from standings;")
    db.commit
    rankings= c.fetchall()
    db.close()
    return rankings

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    db,c = connect()
    c.execute("INSERT INTO matches(winner, loser) VALUES(%s,%s)", 
        (winner, loser))
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
     
    db,c = connect()

    # Get the standings from the view standings
    c.execute("SELECT id, name FROM standings;")
    standings = c.fetchall()

    # Get the number of players
    c.execute("SELECT count(id) AS totalplayers FROM tournament;")
    tp= c.fetchall()

    pairs = []
    for player1, player2 in zip(standings[0::2], standings[1::2]):
        pairs.append((player1[0], player1[1], player2[0], player2[1]))
 
    db.close()
    return pairs
    db.close()
    return pairs


