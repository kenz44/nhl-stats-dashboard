import streamlit as st
import pandas as pd
from functions import get_standings, get_top_points

def main():
    standings = get_standings()
    st.title("Team Stats")

    st.markdown(
        """
        <style>
        div[data-baseweb="select"] > div {
            width: 150px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    if standings:
        team_names = sorted([team['team_abbr'] for team in standings])
        selected_team = st.selectbox("Select a team:", team_names)

        team = next(team for team in standings if team['team_abbr'] == selected_team)

        with st.spinner("Fetching data..."):
            top_players = get_top_points(selected_team)
        
        st.title("Overview")

        col1, col2, col3, col4 = st.columns([1,1,1,1])

        with col1:
            st.markdown(
                f"""
                <div style='text-align: left;'>
                    <img src="{team['logo']}" width="150"><br>
                    <h10 style='margin-top: 10px;
                </div>
                """,
                unsafe_allow_html=True
            )
            st.subheader("Record")
            st.write(f"{team['wins']}-{team['losses']}-{team['ot']}")

        with col2:
            st.subheader("Goals")
            st.write(f"{team['gF_average']}")
            st.write("Per Game")

        with col3:
            st.subheader("GAA")
            st.write(f"{team['gA_average']}")
            st.write("Per Game")

        st.subheader(f"Top 5 Points")
        for player in top_players:
            st.write(f"{player['name']}: {player['points']} pts ({player['goals']} G, {player['assists']} A)")

if __name__ == "__main__":
    main()