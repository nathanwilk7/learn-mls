.headers on
select *, sum(stat_value) as total_stat_value from matches
 inner join snapshots on matches.match_id=snapshots.match_id
 inner join players_in_snapshots on snapshots.snapshot_id=players_in_snapshots.snapshot_id
 inner join stats_for_players_in_snapshots on players_in_snapshots.snapshot_id=stats_for_players_in_snapshots.snapshot_id and
  players_in_snapshots.player_id=stats_for_players_in_snapshots.player_id
 inner join players_in_matches on matches.match_id=players_in_matches.match_id and
  players_in_snapshots.player_id=players_in_matches.player_id
where matches.match_id > 650000 and matches.match_id < 700000
group by matches.match_id, players_in_matches.side, stats_for_players_in_snapshots.stat_name
order by matches.match_id
limit 1;
