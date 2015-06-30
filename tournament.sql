-- Table definitions for the tournament project.
--
-- Clean up any previous tournament databases
DROP DATABASE IF EXISTS tournament;

-- Create the database and tables
CREATE DATABASE tournament;
\connect tournament;

CREATE TABLE players(
  id SERIAL PRIMARY KEY,
  name TEXT
);

CREATE TABLE matches(
  winner INTEGER references players(id),
  loser INTEGER references players(id),
  PRIMARY KEY (winner, loser)
);

-- Create a view that tallies total matches per player
CREATE OR REPLACE VIEW games_view AS
SELECT players.id, COUNT(matches.*) AS games
FROM players LEFT JOIN matches
ON players.id = matches.winner OR players.id = matches.loser
GROUP BY players.id;
