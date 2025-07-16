import requests
import streamlit as st

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
            'team_abbr': get_value(team['teamAbbrev']['default']),
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

def get_all_teams_rosters():
    url = f"https://api-web.nhle.com/v1/teams"
    response = requests.get(url)

    if response.status_code != 200:
        st.error(f"Failed to fetch all teams: {response.status_code}")
        return None
    
    teams = response.json()
    
    rosters = {}
    for team in teams.get('teams', []):
        team_id = team['id']
        team_name = team['name']
        roster_url = f"https://statsapi.web.nhl.com/api/v1/teams/{team_id}/roster"
        roster_response = requests.get(roster_url)
        if roster_response.status_code == 200:
            rosters[team_name] = roster_response.json().get('roster', [])
        else:
            rosters[team_name] = []

    return rosters

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

def get_player_id_by_name(name, rosters):
    name = name.lower()

    for team, players in rosters:
        for player in players:
            fullname = player['person']['fullName'].lower()

            if name in fullname:
                return player['person']['id'], player['person']['fullName']
    return None, None

@st.cache_data(ttl=3600)
def get_player_stats(player_id, season=None):
    url = f"https://api-web.nhle.com/v1/player/{player_id}/landing"
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Failed to fetch roster for player {player_id}: {response.status_code}")
        return []

    data = response.json()

    try:
        # Try to extract regular season stats
        reg_stats = data['featuredStats']['regularSeason']['subSeason']
        
        stats = {
            'reg_season_games_played': reg_stats.get('gamesPlayed', 0),
            'reg_goals': reg_stats.get('goals', 0),
            'reg_assists': reg_stats.get('assists', 0),
            'reg_points': reg_stats.get('points', 0),
            'reg_plus_minus': reg_stats.get('plusMinus', 0),
            'reg_penalty_minutes': reg_stats.get('pim', 0),
            'reg_power_play_goals': reg_stats.get('powerPlayGoals', 0),
            'reg_power_play_points': reg_stats.get('powerPlayPoints', 0),
            'reg_short_handed_goals': reg_stats.get('shorthandedGoals', 0),
            'reg_shots': reg_stats.get('shots', 0),
            'reg_shooting_pctg': reg_stats.get('shootingPctg', 0.0),
        }
    except KeyError:
        # If keys are missing, warn the user and return an empty stats dict (or you can return None)
        print(f"Regular season stats not available for player {player_id}")
        stats = {}
    
    # You might also want to add some basic player info if needed:
    try:
        basic_info = {
            'first_name': data['firstName']['default'],
            'last_name': data['lastName']['default'],
            'headshot': data.get('headshot', None)
        }
    except KeyError:
        basic_info = {}

    # Combine basic info with stats
    player_stats = {**basic_info, **stats}
    return player_stats

def get_top_points(team):
    url = url = f"https://api-web.nhle.com/v1/roster/{team}/current"
    response = requests.get(url)

    if response.status_code != 200:
        return []

    roster = response.json()
    players = roster.get("forwards", []) + roster.get("defensemen", [])

    player_stats = []

    for player in players:
        player_id = player["id"]
        player_name = f"{player['firstName']['default']} {player['lastName']['default']}"
        
        stats_response = get_player_stats(player_id)

        try:
            goals = stats_response.get("reg_goals", 0)
            assists = stats_response.get("reg_assists", 0)
            points = stats_response.get("reg_points", goals + assists)
        except KeyError:
            continue

        player_stats.append({
            "name": player_name,
            "goals": goals,
            "assists": assists,
            "points": points
        })

    # Sort and return top 5
    top_5 = sorted(player_stats, key=lambda x: x["points"], reverse=True)[:5]
    return top_5

# if __name__ == "__main__":
    
#     get_player_id_by_name('Conner McDavid')