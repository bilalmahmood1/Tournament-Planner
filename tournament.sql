
-- Cleaning the old tables in the tournament db
DROP TABLE IF EXISTS matches;
DROP TABLE IF EXISTS teams;

-- Creating new tables:teams and matches

-- table to store all the teams
CREATE TABLE teams(
id serial PRIMARY KEY,
team_name TEXT
);

-- table to store match results
CREATE TABLE matches(
    id SERIAL PRIMARY KEY,
    winner INTEGER REFERENCES teams(id),
    loser INTEGER REFERENCES teams(id)


);
