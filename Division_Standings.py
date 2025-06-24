import streamlit as st
from functions import get_standings

def display_standings_by_division(standings, division_filter):
    # Filter for the specific division
    division_teams = sorted(
        [team for team in standings if team['division'] == division_filter],
        key=lambda x: x['points'],
        reverse=True
    )

    div_leader = division_teams[0]

    col1, col2 = st.columns([1,1])

    with col1:
        st.header(division_filter)
        for team in division_teams:
            st.write(f"{team['team_name']} — {team['points']} pts ({team['wins']}-{team['losses']})")

    with col2:
        st.markdown(
            f"""
            <div style='text-align: center; margin-top: 100px'>
                <img src="{div_leader['logo']}" width="300"><br>
                <h10 style='margin-top: 10px;'>Division Leader: {div_leader['team_name']}</h4>
            </div>
            """,
            unsafe_allow_html=True
        )

def main():
    st.title("NHL Division Standings")

    standings = get_standings()

    division_names = ["Atlantic", "Metropolitan", "Central", "Pacific"]
    tabs = st.tabs(division_names)

    for tab, division in zip(tabs, division_names):
        with tab:
            if standings:
                display_standings_by_division(standings, division)
            else:
                st.error("No standings data to display.")

if __name__ == "__main__":
    main()