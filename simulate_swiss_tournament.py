from tournament import *
from math import log

## starting off the tournament with deleting all the previous matches and player records
deleteMatches()
deletePlayers()

## teams to play
teams = ["LionA","TigerB","CatC","DogD",
        "SpiderE","BirdF","Sparrow_G","DonkeyH",
        "HulkI","SupermanJ","SpidermanK","DeadpoolL",
        "GokuM","VegetaN","KingBobO","GuruP"]

## registering them for the series
for team in teams :
    registerPlayer(team)


print "{} teams got registered for the contest".format(countPlayers())

## play the tournament, random wins assigned
for i in range(int(log(countPlayers(),2))):
    raw_input("Press enter to play round {}".format(i + 1))
    play_a_round()
    display_score()

