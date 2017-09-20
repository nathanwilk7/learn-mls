CREATE TABLE matches (
       competition_id INTEGER,
       season_id INTEGER,
       match_id INTEGER,
       first_half_start INTEGER,
       first_half_stop INTEGER,
       second_half_start INTEGER,
       second_half_stop INTEGER,
       date INTEGER,
       home_id INTEGER,
       home_team_name TEXT,
       away_id INTEGER,
       away_team_name TEXT,
       range_from TEXT DEFAULT NULL,
       range_till TEXT DEFAULT NULL,
       status TEXT,

       PRIMARY KEY (match_id)
);

CREATE TABLE players (
       player_id INTEGER,
       first_name TEXT,
       last_name TEXT,
       known_name TEXT,

       PRIMARY KEY (player_id)
);


CREATE TABLE players_in_matches (
       match_id INTEGER,
       player_id INTEGER,
       side INTEGER,
       team INTEGER,
       position TEXT,
       number TEXT,
       default_position TEXT,

       PRIMARY KEY (match_id, player_id),
       
       FOREIGN KEY (match_id) REFERENCES matches (match_id),
       FOREIGN KEY (player_id) REFERENCES players (player_id)
);

CREATE TABLE snapshots (
       snapshot_id INTEGER PRIMARY KEY,
       match_id INTEGER,
       timestamp INTEGER,
       period TEXT,
       match_time INTEGER,
       score_home INTEGER,
       score_away INTEGER,
       running INTEGER,
       progress INTEGER,
       since_match_began INTEGER,
       f9Id INTEGER,
       relevance INTEGER,
       half_score_home INTEGER,
       half_score_away INTEGER,

       UNIQUE (match_id, timestamp)
);

CREATE TABLE players_in_snapshots (
       snapshot_id INTEGER,
       player_id INTEGER,
       participation INTEGER,
       participation_min INTEGER,
       index_total REAL,
       index_off REAL,
       index_def REAL,

       PRIMARY KEY (snapshot_id, player_id)

       FOREIGN KEY (snapshot_id) REFERENCES snapshots (snapshot_id)
       FOREIGN KEY (player_id) REFERENCES players (player_id)
);

CREATE TABLE stats (
       stat_name TEXT,

       PRIMARY KEY (stat_name)
);

CREATE TABLE stats_for_players_in_snapshots (
       snapshot_id INTEGER,
       player_id INTEGER,
       stat_name TEXT,
       stat_value INTEGER,

       PRIMARY KEY (snapshot_id, player_id, stat_name),

       FOREIGN KEY (snapshot_id, player_id) REFERENCES players_in_snapshots (snapshot_id, player_id), -- valid?
       FOREIGN KEY (stat_name) REFERENCES stats (stat_name)
);
