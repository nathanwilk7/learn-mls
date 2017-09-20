import json
import sqlite3
import pdb

from os import listdir
from os.path import isfile, join

db_path = 'm.db'
matches_path = 'matches/'
match_filenames = [f for f in listdir(matches_path) if isfile(join(matches_path, f))]
file_ext = 'json'

printerval = 10
next_print = printerval

matches_sql = '''
INSERT INTO matches (
competition_id,
season_id,
match_id,
first_half_start,
first_half_stop,
date,
home_id,
home_team_name,
away_id,
away_team_name,
range_from,
range_till,
status
) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)
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
INSERT INTO players_in_matches (
match_id,
player_id,
side,
team,
position,
number
) VALUES (?,?,?,?,?,?)
'''

snapshots_sql = '''
INSERT INTO snapshots (
match_id,
timestamp,
period,
match_time,
score_home,
score_away,
relevance,
half_score_home,
half_score_away
) VALUES (?,?,?,?,?,?,?,?,?)
'''

players_in_snapshots_sql = '''
INSERT INTO players_in_snapshots (
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
INSERT INTO stats_for_players_in_snapshots (
snapshot_id,
player_id,
stat_name,
stat_value
) VALUES (?,?,?,?)
'''

# insert into db
def i_d(c, sql, goods, snap_pk=False, execute_many=False):
   try:
      if execute_many:
         c.executemany(sql, goods)
      else:
         c.execute(sql, goods)
      if snap_pk:
         c.execute('SELECT snapshot_id FROM snapshots WHERE match_id=? AND timestamp=?', (goods[0], goods[1]))
         pk = c.fetchone()[0]
         return pk
   except Exception as e:
      print(e)

match_ids = set()
for match_filename in match_filenames:
   match_id = int(match_filename[:-len(file_ext)-1])
   match_ids.add(match_id)

natee = 0
for match_id in match_ids:
   if next_print == 0:
      print('progress:', round(float(natee) / float(len(match_ids)), 2), '%')
      print('match_id:', match_id)
      next_print = printerval
   natee += 1
   next_print -= 1
   with open('{matches_path}{match_id}.{file_ext}'.format(matches_path=matches_path, match_id=match_id, file_ext=file_ext), 'r') as r:
      m = json.load(r)
   try:
      match = m['match']
      match_teams = match['teams']
      match_teams_home = match_teams['Home']
      match_teams_away = match_teams['Away']
   except KeyError as e:
      print(match_id, "doesn't have field", e)
      continue

   conn = sqlite3.connect(db_path)
   c = conn.cursor()
   try:
      i_d(c,
          matches_sql,
          (match['competitionId'],
           match['seasonId'],
           match['matchId'],
           match['first_half_start'],
           match['first_half_stop'],
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
   except KeyError as e:
      print(match['matchId'], 'does not have field', e)
   stat_index_to_stat_name = {}
   stat_indexes = match['statIndexes']
   for stat_name, stat_index in stat_indexes.items():
      i_d(c,
          stats_sql,
          [stat_name]
      )
      stat_index_to_stat_name[stat_index] = stat_name
   for player_id, player in match['players'].items():
      i_d(c,
          players_sql,
          (player_id,
           player['firstname'],
           player['lastname'],
           player['knownname']
          )
      )
      try:
         i_d(c,
             players_in_matches_sql,
             (match['matchId'],
              player_id,
              player['side'],
              player['team'],
              player['position'],
              player['number']
#              player['defaultPosition']
             )
         )
      except KeyError as e:
         print(match['matchId'], 'does not have field', e)
   for snapshot in match['snapshots']:
      snapshot_id = i_d(c,
                        snapshots_sql,
                        (match['matchId'],
                         snapshot['timestamp'],
                         snapshot['period'],
                         snapshot['matchTime'],
                         snapshot['score_Home'],
                         snapshot['score_Away'],
                         #snapshot['running'],
                         #snapshot['progress'],
                         #snapshot['sinceMatchBegin'],
                         #snapshot['f9Id'],
                         snapshot['relevance'],
                         snapshot['halfscore_Home'],
                         snapshot['halfscore_Away']
                        ),
                        snap_pk=True
      )
      for player_id, player in snapshot['players'].items():
         try:
            i_d(c,
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
         except Exception as e:
            print(match['matchId'], 'does not have', e)
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
         i_d(c,
             stats_for_players_in_snapshots_sql,
             player_stats_list,
             execute_many=True
         )
   conn.commit()
   conn.close()
