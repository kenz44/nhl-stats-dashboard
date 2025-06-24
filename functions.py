import requests

def get_value(obj):
    # If obj is dict with 'default' key, return that, else return obj as string
    if isinstance(obj, dict) and 'default' in obj:
        return obj['default']
    return obj  # already string

def get_standings():
    url = "https://api-web.nhle.com/v1/standings/now"
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Error fetching standings: {response.status_code}")
        return []

    data = response.json()

    standings = []
    for team in data['standings']:
        team_data = {
            'team_name': get_value(team['teamName']),
            'logo': get_value(team['teamLogo']),
            'division': get_value(team['divisionName']),
            'conference': get_value(team['conferenceName']),
            'games_played': team['gamesPlayed'],
            'wins': team['wins'],
            'losses': team['losses'],
            'ot': team['otLosses'],
            'points': team['points'],
            'streak': team.get('streakCode', 'N/A')
        }
        standings.append(team_data)

    return standings

def get_team_roster(team_abbr):
    url = f"https://api-web.nhle.com/v1/roster/{team_abbr}/current"
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Failed to fetch roster for {team_abbr}: {response.status_code}")
        return []

    roster_data = response.json()
    players = roster_data.get('forwards', []) + roster_data.get('defensemen', []) + roster_data.get('goalies', [])

    player_list = []
    for player in players:
        position = player.get('positionCode', 'N/A')
        jersey = player.get('sweaterNumber', 'N/A')

        player_info = {
            'id': player['id'],
            'first_name': player['firstName']['default'],
            'last_name': player['lastName']['default'],
            'position': position,
            'jersey_number': jersey
        }
        player_list.append(player_info)

    return player_list

def get_player_stats(player_id, season=None):
    url = f"https://api-web.nhle.com/v1/player/{player_id}/landing"
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Failed to fetch roster for player {player_id}: {response.status_code}")
        return []

    player_data = response.json()
    player_stats = {
            'player_id': player_id,
            'headshot': player_data['headshot'],
            'first_name': player_data['firstName']['default'],
            'last_name': player_data['lastName']['default'],
            'season': player_data['featuredStats']['season'],
            'reg_season_games_played': player_data['featuredStats']['regularSeason']['subSeason']['gamesPlayed'],
            'reg_goals': player_data['featuredStats']['regularSeason']['subSeason']['goals'],
            'reg_assists': player_data['featuredStats']['regularSeason']['subSeason']['assists'],
            'reg_points': player_data['featuredStats']['regularSeason']['subSeason']['points'],
            'reg_plus_minus': player_data['featuredStats']['regularSeason']['subSeason']['plusMinus'],
            'reg_penalty_minutes': player_data['featuredStats']['regularSeason']['subSeason']['pim'],
            'reg_power_play_goals': player_data['featuredStats']['regularSeason']['subSeason']['powerPlayGoals'],
            'reg_power_play_points': player_data['featuredStats']['regularSeason']['subSeason']['powerPlayPoints'],
            'reg_short_handed_goals': player_data['featuredStats']['regularSeason']['subSeason']['shorthandedGoals'],
            'reg_shots': player_data['featuredStats']['regularSeason']['subSeason']['shots'],
            'reg_shooting_pctg': player_data['featuredStats']['regularSeason']['subSeason']['shootingPctg'],
        }
    
    return player_stats

# if __name__ == "__main__":
#     standings = get_standings()
#     for team in standings:
#         print(f"{team['team_name']} - {team['points']} pts ({team['wins']}-{team['losses']}-{team['ot']})")

    # team = "EDM"
    # roster = get_team_roster(team)
    # for player in roster:
    #     print(f"{player['first_name']} {player['last_name']} - Position: {player['position']} - Jersey #: {player['jersey_number']}")

    # player_stats = get_player_stats(8478402)
    # print(f"{player_stats['first_name']} {player_stats['last_name']} - Games Played: {player_stats['reg_season_games_played']} - headshot link: {player_stats['headshot']}")