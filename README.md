# Project Title: Swiss system based tournament planner

In this project I wrote a python module called tournament.py, with a
database backend, that can be used to track even number of players
and the matches they play with one another in a single tournament.
The game tournament used is intermediate between elimination and
round-robin and is called Swiss system. In this system no player/team
is eliminated and is made to play with an opponent of equal strength
and the winner is one that wins all his matches.

## Installation

### Software

* Install [Anaconda](https://www.continuum.io/downloads) to run the module
* Install [PostgreSQL](https://www.postgresql.org/) to setup database

### Setup

1. Once above softwares are installed, create a database in postgreSQL of the name tournament and run the tournament.sql script to create the tables that would be populated with team names and match results. In addition, make sure postgreSQL is running in the background when you are running the application. **Important : use following credientials while installing postgreSQL _user = postgres password = bilal_**
2. On the python side, Anaconda framework has all the built in libraries that are required to run the module successfully except **tabulate** and thus you need to run the below code to install it from the command line option available in Anaconda: ` pip install tabulate `
3. To use all the functions available in the module use the following code snipet: `from tournament import *`
4. Run tournament_test.py file in Anaconda to check whether everything is working as expected
5. Enjoy organizing your tournament :)

### Sample Use
```
from tournament import *
from math import log
## starting off the tournament with deleting all the previous matches and player records
deleteMatches()
deletePlayers()
## teams to play
teams = ["LionA","TogerB","CatC","DogD",
        "SpiderE","BirdF","Sparrow_G","DonkeyH",
        "HulkI","SupermanJ","SpidermanK","DeadpoolL",
        "GokuM","VegtaN","BobO","GuruP"]

## registering them for the series
for team in teams :
    registerPlayer(team)

print "{} teams got registered for the contest".format(countPlayers())

## play the tournament, random wins assigned
for i in range(int(log(countPlayers(),2))):
    print "Round {}".format(i + 1)
    play_a_round()
    display_score()
```

### License
_MIT License_
# Tournament-Planner
