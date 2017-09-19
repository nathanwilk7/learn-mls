import json
import sqlite3
import pdb

db_path = 'matches.db'
matches_path = 'matches/'
file_ext = 'json'

matches_sql = '''
INSERT OR IGNORE INTO matches (
competition_id,
season_id,
match_id,
first_half_start,
first_half_stop,
second_half_start,
second_half_stop,
date,
home_id,
home_team_name,
away_id,
away_team_name,
range_from,
range_till,
status
) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
'''

players_sql = '''
INSERT OR IGNORE INTO players (
player_id,
first_name,
last_name,
known_name
) VALUES (?,?,?,?)
'''

players_in_matches_sql = '''
INSERT OR IGNORE INTO players_in_matches (
match_id,
player_id,
side,
team,
position,
number,
default_position
) VALUES (?,?,?,?,?,?,?)
'''

snapshots_sql = '''
INSERT INTO snapshots (
match_id,
timestamp,
period,
match_time,
score_home,
score_away,
running,
progress,
since_match_began,
f9Id,
relevance,
half_score_home,
half_score_away
) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)
'''

players_in_snapshots_sql = '''
INSERT OR IGNORE INTO players_in_snapshots (
snapshot_id,
player_id,
participation,
participation_min,
index_total,
index_off,
index_def
) VALUES (?,?,?,?,?,?,?)
'''

stats_sql = '''
INSERT OR IGNORE INTO stats (
stat_name
) VALUES (?)
'''

stats_for_players_in_snapshots_sql = '''
INSERT OR IGNORE INTO stats_for_players_in_snapshots (
snapshot_id,
player_id,
stat_name,
stat_value
) VALUES (?,?,?,?)
'''

# insert into db
def i_d(conn, sql, goods, snap_pk=False, execute_many=False):
   try:
      c = conn.cursor()
      if execute_many:
         c.executemany(sql, goods)
      else:
         c.execute(sql, goods)
      conn.commit()
      if snap_pk:
         c.execute('SELECT snapshot_id FROM snapshots WHERE match_id=? AND timestamp=?', (goods[0], goods[1]))
         pk = c.fetchone()[0]
         return pk
   except Exception as e:
      print(e)

match_ids = ['902128']
for match_id in match_ids:
   with open('{matches_path}{match_id}.{file_ext}'.format(matches_path=matches_path, match_id=match_id, file_ext=file_ext), 'r') as r:
      m = json.load(r)
   match = m['match']
   match_teams = match['teams']
   match_teams_home = match_teams['Home']
   match_teams_away = match_teams['Away']

   conn = sqlite3.connect(db_path)
   
   i_d(conn,
       matches_sql,
       (match['competitionId'],
        match['seasonId'],
        match['matchId'],
        match['first_half_start'],
        match['first_half_stop'],
        match['second_half_start'],
        match['second_half_stop'],
        match['date'],
        match_teams_home['id'],
        match_teams_home['name'],
        match_teams_away['id'],
        match_teams_away['name'],
        match['range']['from'],
        match['range']['till'],
        m['status']
       )
   )
   stat_index_to_stat_name = {}
   stat_indexes = match['statIndexes']
   for stat_name, stat_index in stat_indexes.items():
      i_d(conn,
          stats_sql,
          [stat_name]
      )
      stat_index_to_stat_name[stat_index] = stat_name
   for player_id, player in match['players'].items():
      i_d(conn,
          players_sql,
          (player_id,
           player['firstname'],
           player['lastname'],
           player['knownname']
          )
      )
      i_d(conn,
          players_in_matches_sql,
          (match['matchId'],
           player_id,
           player['side'],
           player['team'],
           player['position'],
           player['number'],
           player['defaultPosition']
          )
      )
   for snapshot in match['snapshots']:
      snapshot_id = i_d(conn,
                        snapshots_sql,
                        (match['matchId'],
                         snapshot['timestamp'],
                         snapshot['period'],
                         snapshot['matchTime'],
                         snapshot['score_Home'],
                         snapshot['score_Away'],
                         snapshot['running'],
                         snapshot['progress'],
                         snapshot['sinceMatchBegin'],
                         snapshot['f9Id'],
                         snapshot['relevance'],
                         snapshot['halfscore_Home'],
                         snapshot['halfscore_Away']
                        ),
                        snap_pk=True
      )
      for player_id, player in snapshot['players'].items():
         i_d(conn,
             players_in_snapshots_sql,
             (snapshot_id,
              player_id,
              player['participation'],
              player['participationMin'],
              player['index']['total'],
              player['index']['off'],
              player['index']['def']
             )
         )
         player_stats = player['stats']
         player_stats_list = []
         for i in range(len(player_stats)):
            stat_value = player_stats[i]
            player_stats_list.append(
               (
                  snapshot_id,
                  player_id,
                  stat_index_to_stat_name[i],
                  stat_value
               )
            )
         print('player id: ', player_stats_list[0][1])
         i_d(conn,
             stats_for_players_in_snapshots_sql,
             player_stats_list,
             execute_many=True
         )
                 
   conn.close()
