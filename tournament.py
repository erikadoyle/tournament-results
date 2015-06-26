#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import itertools


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    pgsql = connect()
    cursor = pgsql.cursor()
    cursor.execute("delete from matches")
    pgsql.commit()
    pgsql.close()


def deletePlayers():
    """Remove all the player records from the database."""
    pgsql = connect()
    cursor = pgsql.cursor()
    cursor.execute("delete from players")
    pgsql.commit()
    pgsql.close()


def countPlayers():
    """Returns the number of players currently registered."""
    pgsql = connect()
    cursor = pgsql.cursor()
    cursor.execute("select count(*) as total from players")
    total = cursor.fetchone()
    pgsql.close()
    return total[0]


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.

    Args:
      name: the player's full name (need not be unique).
    """
    """Returns the number of players currently registered."""
    pgsql = connect()
    cursor = pgsql.cursor()
    cursor.execute("insert into players (name) values (%s)", (name,))
    pgsql.commit()
    pgsql.close()
    return countPlayers()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a
    player tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    pgsql = connect()
    cursor = pgsql.cursor()
    # Union all technique discovered via http://stackoverflow.com/questions/
    # 30091148/postgresql-display-and-count-distinct-occurrences-of-values
    # -across-multiple-col
    cursor.execute("select id, name, count(matches.winner) as wins,"
                   "(select count(*) as games from("
                   "    select p1 as pid from matches"
                   "    union all select p2 from matches"
                   ") games where games.pid = players.id) "
                   "from players left join matches "
                   "on players.id = matches.winner "
                   "group by players.id, players.name "
                   "order by wins desc")

    playerslist = cursor.fetchall()
    pgsql.close()
    return playerslist


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    pgsql = connect()
    cursor = pgsql.cursor()
    cursor.execute("insert into matches (p1, p2, winner) values (%s, %s, %s)",
                   (winner, loser, winner))
    pgsql.commit()
    pgsql.close()


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
    standings = playerStandings()

    # Pair off every two entries in the player standings in a new list
    # Discovered via http://stackoverflow.com/questions/434287/
    # what-is-the-most-pythonic-way-to-iterate-over-a-list-in-chunks
    pairingsiterator = itertools.izip(*[iter(standings)]*2)

    # Iterate through the list and build the pairings
    results = []
    pairings = list(pairingsiterator)
    for pair in pairings:
        id1 = pair[0][0]
        name1 = pair[0][1]
        id2 = pair[1][0]
        name2 = pair[1][1]
        matchup = (id1, name1, id2, name2)
        results.append(matchup)
    return results
