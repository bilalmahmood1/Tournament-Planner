#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament planner
# author: Bilal Mahmood


import psycopg2
from tabulate import tabulate

def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""

    ## to run locally
    return psycopg2.connect("dbname=tournament user = postgres password = bilal")

    ## return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""

    ## connecting with db
    db = connect()
    ## creating a cursor object
    c = db.cursor()
    ## query to execute
    query = ''' delete from matches'''
    ## execute the query
    c.execute(query)
    ## commite changes in the database
    db.commit()
    ## closing the connection with the database
    db.close()


def deletePlayers():
    """Remove all the player records from the database."""

    ## wiping out the matches table
    deleteMatches()
    ## connecting with db
    db = connect()
    ## creating a cursor object
    c = db.cursor()
    ## remove all the rows in teams
    query = ''' delete from teams '''
    ## execute the query
    c.execute(query)
    ## commite changes in the database
    db.commit()
    ## closing the connection with the database
    db.close()



def countPlayers():
    """Returns the number of players currently registered."""
    ## connecting with db
    db = connect()
    ## creating a cursor object
    c = db.cursor()
    ## query to execute
    query = ''' select count(*) from teams '''
    ## execute the query
    c.execute(query)
    ## query result
    result = c.fetchall()
    ## closing the connection with the database
    db.close()
    number_players = result[0][0]
    return number_players



def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    ## connecting with db
    db = connect()
    ## creating a cursor object
    c = db.cursor()
    ## insert into the teams table player name
    c.execute('insert into teams (team_name) values (%s)',(name,))
    ## commite changes in the database
    db.commit()
    ## closing the connection with the database
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

    ## connecting with db
    db = connect()
    ## creating a cursor object
    c = db.cursor()
    ## get the scores table from the matches table using the below sql query
    query = '''
    SELECT wins_table.id, wins_table.team_name, wins_table.wins,
    wins_table.wins + loses_table.loses as total FROM
    (SELECT TEAMS.*, (SELECT COUNT(*) FROM MATCHES WHERE MATCHES.winner = TEAMS.id)
        AS WINS FROM TEAMS) as wins_table,
    (SELECT TEAMS.*, (SELECT COUNT(*) FROM MATCHES WHERE MATCHES.loser = TEAMS.id)
        AS LOSES FROM TEAMS) as loses_table
    WHERE wins_table.id = loses_table.id
    ORDER BY wins_table.wins desc;
    '''
    ## execute the query
    c.execute(query)
    ## query result
    result = c.fetchall()

    ## closing the connection with the database
    db.close()
    return result

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """

    ## connecting with db
    db = connect()
    ## creating a cursor object
    c = db.cursor()
    ## lets update the games table
    c.execute(''' insert into matches (winner,loser) values(%s,%s) ''',(winner, loser))
    db.commit()

    ## closing the connection with the database
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
    ## sorted score table
    score_table = playerStandings()
    ## simple pairing in which I am pairing the nearest pairs together
    ## by taking a sorted scores table and then picking up pair
    ## of players from there. I am making an assumption that there
    ## are even players
    players = len(score_table)
    next_round_matches = []
    for i in range(0,players,2):
        pair = (score_table[i][0],score_table[i][1],
                score_table[i + 1][0],score_table[i + 1][1])

        next_round_matches.append(pair)


    return next_round_matches


def display_score():
    """ This function displays the score card in a nice looking
	format on the console"""
    points_table = playerStandings()

    score_board = []
    for team in points_table:
        score_board.append([ i for i in team])

    print tabulate(score_board,headers = ["ID","Team Name","Wins","Total Matches"],tablefmt="fancy_grid")


def play_a_round():
    """ This function simulates one round in swiss based tournament;assigning
	win to left player in each pair"""
    ## get the teams that would play in next round match
    pairs = swissPairings()
    for match in pairs:
        ## play a match
        winner = match[0]
        loser = match[2]
        ## report the result
        reportMatch(winner, loser)