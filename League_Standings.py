import streamlit as st
import pandas as pd
from functions import get_standings

def display_standings_table(standings, division_filter=None, conference_filter=None):
    if division_filter:
        filtered_teams = [team for team in standings if team['division'] == division_filter]
    elif conference_filter:
        filtered_teams = [team for team in standings if team['conference'] == conference_filter]
    else:
        filtered_teams = standings

    filtered_teams = sorted(filtered_teams, key=lambda x: x['points'], reverse=True)

    if not filtered_teams:
        st.warning("No teams found for the given filter")
        return

    df_rows = []
    for team in filtered_teams:
        row = {
            "Logo": f'<img src="{team["logo"]}" width="40">',
            "Team": team['team_name'],
            "GP": team['games_played'],
            "W": team['wins'],
            "L": team['losses'],
            "OT": team['ot'],
            "PTS": team['points'],
            "DIFF": team['wins'] - team['losses'],
        }

        # stats if viewing by conference
        if conference_filter:
            row.update({
                "GF": team['gF'],
                "GA": team['gA'],
                "L10": team['last10'],
                "winPctg": round(team['winPctg'] * 100),
                "Streak": team['streak']
            })

        df_rows.append(row)

    df = pd.DataFrame(df_rows)

    st.subheader(division_filter or conference_filter or "Standings")

    st.markdown(df.to_markdown(index=False), unsafe_allow_html=True)

def main():
    st.set_page_config(layout="wide") 
    st.title("Division Standings")

    standings = get_standings()
    if not standings:
        st.error("Failed to load standings data.")
        return

    division_names = ["Atlantic", "Metropolitan", "Central", "Pacific"]

    row1 = st.columns(2)
    row2 = st.columns(2)
    grid = row1 + row2

    for division, col in zip(division_names, grid):
        with col:
            display_standings_table(standings, division_filter=division)

    st.title("Conference Statistics")

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

    conferences = ['Western', 'Eastern']
    selected_conference = st.selectbox("Select a conference:", conferences)

    display_standings_table(standings, conference_filter=selected_conference)


if __name__ == "__main__":
    main()
