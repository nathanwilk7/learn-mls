.mode column
.headers on

select home_team_name, stat_name, sum(stat_value), side from matches
       inner join snapshots on matches.match_id=snapshots.match_id
       inner join players_in_snapshots on snapshots.snapshot_id=players_in_snapshots.snapshot_id
       inner join stats_for_players_in_snapshots on players_in_snapshots.snapshot_id=stats_for_players_in_snapshots.snapshot_id and
       	     	  				    players_in_snapshots.player_id=stats_for_players_in_snapshots.player_id
	inner join players_in_matches on matches.match_id=players_in_matches.match_id and
	      	   		      	 players_in_snapshots.player_id=players_in_matches.player_id
where (home_team_name='Real Salt Lake' and side='Home') and season_id=2017
group by home_team_name, stat_name;
--group by (home_team_name);
