import csv
import pdb
import sqlite3

# connect to db

db_path = 'm.db'
output_path = 'matches.csv'
min_match_id = 650000
max_match_id = 1000001 #1000000
matcherval = 5000

match_fieldnames = [
    'match_id',
    'competition_id',
    'season_id',
    'date',
    'home_team_name',
    'away_team_name',
    'score_home',
    'score_away',
    'half_score_home',
    'half_score_away',
    'num_players'
]

match_stats_sql = '''
select *, 
 sum(stat_value) as total_stat_value, 
 count(distinct players_in_snapshots.player_id) as num_players from matches
 inner join snapshots on matches.match_id=snapshots.match_id
 inner join players_in_snapshots on snapshots.snapshot_id=players_in_snapshots.snapshot_id
 inner join stats_for_players_in_snapshots on players_in_snapshots.snapshot_id=stats_for_players_in_snapshots.snapshot_id and
  players_in_snapshots.player_id=stats_for_players_in_snapshots.player_id
 inner join players_in_matches on matches.match_id=players_in_matches.match_id and
  players_in_snapshots.player_id=players_in_matches.player_id
where matches.match_id >= {temp_min_match_id} and matches.match_id < {temp_max_match_id}
group by matches.match_id, players_in_matches.side, stats_for_players_in_snapshots.stat_name
order by matches.match_id;
'''

conn = sqlite3.connect(db_path)
conn.row_factory = sqlite3.Row
c = conn.cursor()

matches = {}
temp_min_match_id = min_match_id
while (temp_min_match_id < max_match_id):
    temp_max_match_id = temp_min_match_id + matcherval
    print(temp_min_match_id, temp_max_match_id)

    c.execute(match_stats_sql.format(temp_min_match_id=temp_min_match_id, temp_max_match_id=temp_max_match_id))
    
    for match_stat in c:
        match_id = match_stat['match_id']
        if match_id in matches:
            match = matches[match_id]
        else:
            match = {}
            for fieldname in match_fieldnames:
                match[fieldname] = match_stat[fieldname]
        match[match_stat['side'].lower() + '_' + match_stat['stat_name'].lower()] = match_stat['total_stat_value']
        matches[match_id] = match
    temp_min_match_id += matcherval

with open(output_path, 'w') as csvfile:
    if len(matches) > 0:
        fieldnames = list(list(matches.values())[0].keys())
    else:
        pdb.set_trace()
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for match_id, match in matches.items():
        writer.writerow(match)

conn.close()
