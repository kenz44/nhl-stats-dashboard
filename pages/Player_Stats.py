import streamlit as st
from functions import get_player_stats

st.title("NHL Player Stats Dashboard")

player_id = st.text_input("Enter Player ID (e.g., 8478402 for Connor McDavid)")

if player_id:
    stats = get_player_stats(int(player_id))
    if stats:
        col1, col2 = st.columns([1, 3])

        with col1:
            st.image(stats['headshot'], width=250)
        with col2:
            st.subheader(f"{stats['first_name']} {stats['last_name']} ({stats['season']})")
            st.write({
                "Games Played": stats['reg_season_games_played'],
                "Goals": stats['reg_goals'],
                "Assists": stats['reg_assists'],
                "Points": stats['reg_points'],
                "Plus/Minus": stats['reg_plus_minus'],
                "Penalty Minutes": stats['reg_penalty_minutes'],
                "PP Goals": stats['reg_power_play_goals'],
                "PP Points": stats['reg_power_play_points'],
                "SH Goals": stats['reg_short_handed_goals'],
                "Shots": stats['reg_shots'],
                "Shooting %": round(stats['reg_shooting_pctg'] * 100, 2),
            })
    else:
        st.error("Failed to retrieve stats.")