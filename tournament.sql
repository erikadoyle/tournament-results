-- Table definitions for the tournament project.

-- Create the database and tables
CREATE DATABASE tournament;
\connect tournament;

CREATE TABLE players(
  id SERIAL UNIQUE,
  name TEXT
);

CREATE TABLE matches(
  p1 INTEGER references players(id),
  p2 INTEGER references players(id),
  winner INTEGER references players(id)
);
