import streamlit as st
import pandas as pd
from functions import get_standings, get_top_points

def main():
    standings = get_standings()

    st.title("Team Stats")

    if standings:
        team_names = sorted([team['team_name'] for team in standings])
        selected_team_name = st.selectbox("Select a team:", team_names)

        selected_team = next(team for team in standings if team['team_name'] == selected_team_name)

        with st.spinner("Fetching top players..."):
            top_players = get_top_points(selected_team['team_abbr'])
        
        st.subheader(f"Top 5 Points")
        for player in top_players:
            st.write(f"{player['name']}: {player['points']} pts ({player['goals']} G, {player['assists']} A)")

        df = pd.DataFrame(top_players)
        st.bar_chart(df.set_index("name")["points"])

if __name__ == "__main__":
    main()