SELECT
  *
FROM
  metadata;

SELECT
  *
FROM
  week;

SELECT
  *
FROM
  position;

SELECT
  s.rowid,
  *
FROM
  stat s
  JOIN stat_position_type stp ON stp.stat_id = s.rowid;

SELECT
  *
FROM
  stat_position_type;

SELECT
  *
FROM
  player;

SELECT
  *
FROM
  player_position;

SELECT
  count(*)
FROM
  player_stat;

SELECT
  *
FROM
  player_stat
  JOIN player ON player.rowid = player_stat.player_id
  JOIN stat ON stat.rowid = player_stat.stat_id
WHERE
  stat.abbr = 'PPG'
  AND stat.value > 0;

SELECT
  *
FROM
  team;

SELECT
  *
FROM
  matchup_team;

SELECT
  *
FROM
  draft_pick;

SELECT
  *
FROM
  transaction_ t
  JOIN transaction_player tp ON tp.transaction_id = t.rowid
  JOIN player p ON p.rowid = tp.player_id
ORDER BY
  t.timestamp_ DESC;

SELECT
  *
FROM
  transaction_player
  JOIN player on player.rowid = transaction_player.player_id
  LEFT JOIN team t1 on t1.rowid = transaction_player.from_team_id
  LEFT JOIN team t2 on t2.rowid = transaction_player.to_team_id
ORDER BY
  transaction_id ASC;

-- Test that goalies arent getting credit for assists
SELECT
  *
FROM
  player_stat
  JOIN player ON player.rowid = player_stat.player_id
WHERE
  stat_id = 2
SELECT
  p.first_name,
  p.last_name,
  s.abbr,
  SUM(ps.value) as tot
FROM
  player p
  JOIN player_stat ps ON ps.player_id = p.rowid
  JOIN stat s ON s.rowid = ps.stat_id
WHERE
  abbr = 'P'
GROUP BY
  p.rowid
ORDER BY
  tot DESC;

-- OTHER
SELECT
  *
FROM
  player
  JOIN player_position on player_position.player_id = player.rowid
  JOIN position on player_position.position_id = position.rowid
WHERE
  last_name = 'Konecny';

SELECT
  *
FROM
  player
WHERE
  last_name = 'Murray';

SELECT
  count(*)
FROM
  player
WHERE
  external_id is not NULL;

-- DEEPSEEK
WITH RECURSIVE
  weeks (week_start) AS (
    SELECT
      DATE(MIN(date), 'weekday 1', '-7 days') -- Weeks start on Monday
    FROM
      goals
    UNION ALL
    SELECT
      DATE(week_start, '+7 days')
    FROM
      weeks
    WHERE
      week_start < (
        SELECT
          MAX(date)
        FROM
          goals
      )
  ),
  -- Combine all team events (adds/drops) in chronological order
  TeamEvents AS (
    SELECT
      team_id,
      player_id,
      draft_date AS event_date,
      'add' AS action
    FROM
      drafts
    WHERE
      team_id = ? -- Your team ID
    UNION ALL
    SELECT
      team_id,
      player_id,
      transaction_date AS event_date,
      action
    FROM
      waivers
    WHERE
      team_id = ? -- Your team ID
  ),
  -- Order events and pair adds with subsequent drops
  OrderedEvents AS (
    SELECT
      team_id,
      player_id,
      event_date,
      action,
      ROW_NUMBER() OVER (
        PARTITION BY
          team_id,
          player_id
        ORDER BY
          event_date,
          CASE
            WHEN action = 'add' THEN 0
            ELSE 1
          END -- Prioritize adds first
      ) AS rn
    FROM
      TeamEvents
  ),
  PairedEvents AS (
    SELECT
      a.team_id,
      a.player_id,
      a.event_date AS add_date,
      COALESCE(d.event_date, '9999-12-31') AS drop_date
    FROM
      OrderedEvents a
      LEFT JOIN OrderedEvents d ON a.team_id = d.team_id
      AND a.player_id = d.player_id
      AND d.rn = a.rn + 1
      AND d.action = 'drop'
    WHERE
      a.action = 'add'
  )
  -- Calculate weekly goals
SELECT
  w.week_start,
  DATE(w.week_start, '+6 days') AS week_end,
  COALESCE(SUM(g.goals), 0) AS total_goals
FROM
  weeks w
  LEFT JOIN PairedEvents pe ON pe.team_id = ? -- Your team ID
  AND pe.add_date <= DATE(w.week_start, '+6 days') -- Overlap check
  AND pe.drop_date >= w.week_start
  LEFT JOIN goals g ON pe.player_id = g.player_id
  AND g.date BETWEEN pe.add_date AND pe.drop_date -- Goals during active period
  AND g.date BETWEEN w.week_start AND DATE(w.week_start, '+6 days') -- Goals during the week
GROUP BY
  w.week_start
ORDER BY
  w.week_start;
