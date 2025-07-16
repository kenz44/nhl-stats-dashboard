import streamlit as st
from functions import get_player_stats, get_player_id_by_name, get_all_teams_rosters

def main():
    st.title("NHL Player Stats Dashboard")

    rosters = get_all_teams_rosters()
    if rosters is None:
        st.error("Failed to load team rosters.")
        return

    player_name = st.text_input("Enter Player First and Last Name (e.g., Connor McDavid)")

    if player_name and rosters:
        player_id, fullname = get_player_id_by_name(player_name, rosters)

        if player_id is None:
            st.error("Player not found. Please check the spelling and try again.")
            return

        stats = get_player_stats(player_id)
        if stats:
            col1, col2 = st.columns([1, 3])
            with col1:
                if stats['headshot']:
                    st.image(stats['headshot'], width=250)
                else:
                    st.text("No image available")
            with col2:
                st.subheader(f"{stats['first_name']} {stats['last_name']} ({stats['season']})")
                st.write({
                    "Games Played": stats.get('reg_season_games_played', 'N/A'),
                    "Goals": stats.get('reg_goals', 'N/A'),
                    "Assists": stats.get('reg_assists', 'N/A'),
                    "Points": stats.get('reg_points', 'N/A'),
                    "Plus/Minus": stats.get('reg_plus_minus', 'N/A'),
                    "Penalty Minutes": stats.get('reg_penalty_minutes', 'N/A'),
                    "PP Goals": stats.get('reg_power_play_goals', 'N/A'),
                    "PP Points": stats.get('reg_power_play_points', 'N/A'),
                    "SH Goals": stats.get('reg_short_handed_goals', 'N/A'),
                    "Shots": stats.get('reg_shots', 'N/A'),
                    "Shooting %": round(stats.get('reg_shooting_pctg', 0.0) * 100, 2),
                })
        else:
            st.error("Failed to retrieve stats.")
    else:
        st.warning("Player not found. Please check the spelling.")

if __name__ == "__main__":
    main()