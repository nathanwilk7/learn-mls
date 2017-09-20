.mode column
.headers on

select distinct * from matches
inner join snapshots on matches.match_id
inner join players_in_snapshots on snapshots.snapshot_id
inner join stats_for_players_in_snapshots on players_in_snapshots.snapshot_id=stats_for_players_in_snapshots.snapshot_id and
      	   				     players_in_snapshots.player_id=stats_for_players_in_snapshots.player_id
where (home_team_name='Real Salt Lake' or away_team_name='Real Salt Lake') and season_id=2017 and date < 1501372800
limit 2;
