from queries import get_yahoo_query

LEAGUE_ID = 76201
GAME_CODE = "nhl"
yq = get_yahoo_query(LEAGUE_ID, game_id=453)

yq.get_league_matchups_by_week(1)

yq.get_league_settings()

yq.get_current_game_info()

players = yq.get_league_players(player_count_limit=100)
players[5]

play = None
for p in yq.get_league_players():
    if p.name.last == "Boldy":
        play = p

play

yq.get_current_game_info().roster_positions

import os

cwd = os.getcwd()
fname = ".env"
abspath = os.path.join(cwd, fname)
os.path.isfile(abspath)


import datetime

from yfpy_nhl_sqlite.main import get_importer_for_db

importer = get_importer_for_db(76201, debug_logging=True)
importer._set_stat_id_lookups()
dt = datetime.date(2024, 12, 20)

rows = importer._get_player_stat_rows_for_date(dt)

importer._player_id_lookup

importer._stat_id_lookup

importer.yq.get_player_stats_by_date("453.p.4935", dt, limit_to_league_stats=False)

importer.yq.get_player_stats_by_date("453.p.7083", dt, limit_to_league_stats=False)

keys = ["453.p.5774", "453.p.9516"]
importer._find_player_id_by_date_stat(keys, dt, 25, 24)
