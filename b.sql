.mode column
.headers on

--select stat_name from stats limit 10;
--select distinct home_team_name from matches;
--.schema
--select distinct side from players_in_matches;

select away_team_name, stat_name, sum(stat_value), side from matches
       inner join snapshots on matches.match_id=snapshots.match_id
       inner join players_in_snapshots on snapshots.snapshot_id=players_in_snapshots.snapshot_id
       inner join stats_for_players_in_snapshots on players_in_snapshots.snapshot_id=stats_for_players_in_snapshots.snapshot_id and
       	     	  				    players_in_snapshots.player_id=stats_for_players_in_snapshots.player_id
	inner join players_in_matches on matches.match_id=players_in_matches.match_id and
	      	   		      	 players_in_snapshots.player_id=players_in_matches.player_id
where (away_team_name='Real Salt Lake' and side='Away') and season_id=2017
group by away_team_name, stat_name;
