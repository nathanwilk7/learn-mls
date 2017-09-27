.mode column
.headers on

--select home_team_name, stat_name, sum(stat_value), side from matches
--       inner join snapshots on matches.match_id=snapshots.match_id
--       inner join players_in_snapshots on snapshots.snapshot_id=players_in_snapshots.snapshot_id
--       inner join stats_for_players_in_snapshots on players_in_snapshots.snapshot_id=stats_for_players_in_snapshots.snapshot_id and
--       	     	  				    players_in_snapshots.player_id=stats_for_players_in_snapshots.player_id
--	inner join players_in_matches on matches.match_id=players_in_matches.match_id and
--	      	   		      	 players_in_snapshots.player_id=players_in_matches.player_id
--where (home_team_name='Real Salt Lake' and side='Home') and season_id=2017
--group by home_team_name, stat_name;

--select away_team_name, stat_name, sum(stat_value), side from matches
--       inner join snapshots on matches.match_id=snapshots.match_id
--       inner join players_in_snapshots on snapshots.snapshot_id=players_in_snapshots.snapshot_id
--       inner join stats_for_players_in_snapshots on players_in_snapshots.snapshot_id=stats_for_players_in_snapshots.snapshot_id and
--       	     	  				    players_in_snapshots.player_id=stats_for_players_in_snapshots.player_id
--	inner join players_in_matches on matches.match_id=players_in_matches.match_id and
--	      	   		      	 players_in_snapshots.player_id=players_in_matches.player_id
--where (away_team_name='Real Salt Lake' and side='Away') and season_id=2017
--group by away_team_name, stat_name;

-- * 1.0 to make it floating point division instead of integer division
select home_team_name as team_name, home_stat_name as stat_name, (home_stat_sum + away_stat_sum) as stat_sum, ((home_stat_avg + away_stat_avg) / 2.0) as stat_avg from (
(select home_team_name, stat_name as home_stat_name, sum(stat_value) as home_stat_sum, (sum(stat_value) / (count(distinct matches.match_id) * 1.0)) as home_stat_avg from matches
       inner join snapshots on matches.match_id=snapshots.match_id
       inner join players_in_snapshots on snapshots.snapshot_id=players_in_snapshots.snapshot_id
       inner join stats_for_players_in_snapshots on players_in_snapshots.snapshot_id=stats_for_players_in_snapshots.snapshot_id and
       	     	  				    players_in_snapshots.player_id=stats_for_players_in_snapshots.player_id
	inner join players_in_matches on matches.match_id=players_in_matches.match_id and
	      	   		      	 players_in_snapshots.player_id=players_in_matches.player_id
where ((home_team_name='Real Salt Lake' and side='Home') or (home_team_name='Seattle Sounders FC' and side='Home')) and season_id=2017
group by home_team_name, stat_name) as home_stats
inner join 
(select away_team_name, stat_name as away_stat_name, sum(stat_value) as away_stat_sum, (sum(stat_value) / (count(distinct matches.match_id) * 1.0)) as away_stat_avg from matches
       inner join snapshots on matches.match_id=snapshots.match_id
       inner join players_in_snapshots on snapshots.snapshot_id=players_in_snapshots.snapshot_id
       inner join stats_for_players_in_snapshots on players_in_snapshots.snapshot_id=stats_for_players_in_snapshots.snapshot_id and
       	     	  				    players_in_snapshots.player_id=stats_for_players_in_snapshots.player_id
	inner join players_in_matches on matches.match_id=players_in_matches.match_id and
	      	   		      	 players_in_snapshots.player_id=players_in_matches.player_id
where ((away_team_name='Real Salt Lake' and side='Away') or (away_team_name='Seattle Sounders FC' and side='Away')) and season_id=2017
group by away_team_name, stat_name) as away_stats
on home_stats.home_stat_name=away_stats.away_stat_name)
group by home_stat_name, home_team_name;
