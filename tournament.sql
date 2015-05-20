-- Table definitiONs for the tournament project.
--
--drop the databASe if it exists
DROP DATABASE if exists tournament;

--create the databASe called tournament
CREATE DATABASE tournament;

\c tournament;

--create the table called tournament
CREATE TABLE tournament ( 
	id serial PRIMARY KEY, 
	name text);

--create the table called matches
CREATE TABLE matches (
	matchNumber serial PRIMARY KEY, 
	winner integer REFERENCES tournament(id), 
	loser integer REFERENCES tournament(id));

--create a view of the wins
CREATE VIEW wins AS SELECT id, name, count(winner) AS wins 
	FROM tournament LEFT JOIN matches ON tournament.id = matches.winner 
	GROUP BY id ORDER BY wins DESC;

--create a view of the losses
CREATE VIEW losses AS SELECT id, count(loser) AS losses 
	FROM tournament LEFT JOIN matches ON tournament.id = matches.loser 
	GROUP BY id ORDER BY losses DESC;

--create a view combining the wins and losses into ONe view	
CREATE VIEW totalMatches AS SELECT wins.id,name,wins,losses 
	FROM wins, losses WHERE wins.id = losses.id;

--create a view of the player id and total matches played
CREATE VIEW totals AS SELECT wins.id, sum(wins + losses) AS total 
	FROM wins, losses WHERE wins.id = losses.id GROUP BY wins.id;

--create a view of the player standings. It will show the id, name, wins, total matches played
CREATE VIEW standings AS SELECT totalMatches.id,name,wins, total 
	FROM totalMatches LEFT JOIN totals ON totalMatches.id = totals.id ORDER BY wins DESC;
