# gui/app.py
import streamlit as st
import requests

MANAGEMENT_BASE = "http://management_service:8000"
SCOREBOARD_BASE = "http://scoreboard_service:8000"
ANALYTICS_BASE  = "http://analytics_service:8000"

st.set_page_config(page_title="Sports Tracker App", layout="wide")
auth_mode = st.sidebar.radio("Authentication", ["Login", "Register"])
if auth_mode == "Register":
    st.sidebar.header("Register")
    reg_username = st.sidebar.text_input("Username", key="reg_username")
    reg_password = st.sidebar.text_input("Password", type="password", key="reg_password")
    if st.sidebar.button("Register"):
        # Send a registration request
        payload = {"username": reg_username, "password": reg_password}
        reg_resp = requests.post(f"{MANAGEMENT_BASE}/register", json=payload)
        if reg_resp.status_code in (200, 201):
            st.sidebar.success("Registration successful! Please log in.")
        else:
                # Print the status code and raw text BEFORE parsing JSON
            print("DEBUG REGISTRATION:", reg_resp.status_code, reg_resp.text)

            try:
                # Attempt to parse the response as JSON
                error_json = reg_resp.json()
                detail = error_json.get("detail", reg_resp.text)
            except ValueError:
                # If JSON parse fails, fallback to raw text
                detail = reg_resp.text
            st.sidebar.error(f"Registration failed: {reg_resp.json().get('detail', reg_resp.text)}")
    st.stop()  

# If in login mode (or after registration, the user switches to login)
if "access_token" not in st.session_state:
    st.sidebar.header("Login")
    login_username = st.sidebar.text_input("Username", key="login_username")
    login_password = st.sidebar.text_input("Password", type="password", key="login_password")
    if st.sidebar.button("Login"):
        # Note: OAuth2PasswordRequestForm usually sends form data, so we use data= instead of json=
        data = {"username": login_username, "password": login_password}
        login_resp = requests.post(f"{MANAGEMENT_BASE}/login", data=data)
        if login_resp.status_code == 200:
            token = login_resp.json().get("access_token")
            st.session_state["access_token"] = token
            st.sidebar.success("Logged in!")
            st.experimental_rerun()
        else:
            st.sidebar.error("Login failed. Please check your credentials.")
    st.stop()  
if "access_token" in st.session_state:
    if st.sidebar.button("Logout"):
        del st.session_state["access_token"]
        st.experimental_rerun()

    
# Simple navigation using a sidebar
page = st.sidebar.selectbox("Select Page", ["Management", "Scoreboard", "Analytics"])

# -------------------------------------------------------------------
# Management Page
# -------------------------------------------------------------------
if page == "Management":
    st.title("Management Service")

    st.subheader("1. Leagues")
    # Fetch leagues
    resp = requests.get(f"{MANAGEMENT_BASE}/leagues")
    if resp.status_code == 200:
        leagues = resp.json()  # list of leagues
        st.write(leagues)
    else:
        st.error("Failed to fetch leagues")

    # Create new league form
    with st.form("create_league"):
        st.write("Create a new league")
        league_name = st.text_input("League Name")
        league_country = st.text_input("Country")
        if st.form_submit_button("Create League"):
            if league_name.strip():
                # POST to create league
                payload = {"name": league_name, "country": league_country}
                create_resp = requests.post(f"{MANAGEMENT_BASE}/leagues", json=payload)
                if create_resp.status_code == 200 or create_resp.status_code == 201:
                    st.success("League created!")
                else:
                    st.error(f"Failed: {create_resp.text}")

    st.subheader("2. Teams")
    resp_teams = requests.get(f"{MANAGEMENT_BASE}/teams")
    if resp_teams.status_code == 200:
        teams = resp_teams.json()
        st.write(teams)
    else:
        st.error("Failed to fetch teams")

    # Create new team form
    with st.form("create_team"):
        st.write("Create a new team")
        team_name = st.text_input("Team Name")
        city_name = st.text_input("City")
        # Let user select a league for the team (optional if your schema allows team w/o league)
        league_options = [l["id"] for l in leagues] if isinstance(leagues, list) else []
        selected_league = st.selectbox("League ID", [None] + league_options)
        if st.form_submit_button("Create Team"):
            if team_name.strip() and city_name.strip():
                team_payload = {
                    "name": team_name,
                    "city": city_name,
                    "league_id": selected_league
                }
                create_team_resp = requests.post(f"{MANAGEMENT_BASE}/teams", json=team_payload)
                if create_team_resp.status_code == 200 or create_team_resp.status_code == 201:
                    st.success("Team created!")
                else:
                    st.error(f"Failed: {create_team_resp.text}")

    st.subheader("3. Matches")
    resp_matches = requests.get(f"{MANAGEMENT_BASE}/matches")
    if resp_matches.status_code == 200:
        matches = resp_matches.json()
        st.write(matches)
    else:
        st.error("Failed to fetch matches")

    # Create new match
    with st.form("create_match"):
        st.write("Create a new match")
        # Re-fetch teams if needed for selection
        team_options = []
        if isinstance(teams, list):
            team_options = [t["id"] for t in teams]
        league_options = [l["id"] for l in leagues] if isinstance(leagues, list) else []

        selected_league_for_match = st.selectbox("League ID for match", league_options)
        home_team = st.selectbox("Home Team ID", team_options)
        away_team = st.selectbox("Away Team ID", team_options)
        if st.form_submit_button("Create Match"):
            if home_team and away_team and home_team != away_team:
                match_payload = {
                    "league_id": selected_league_for_match,
                    "home_team_id": home_team,
                    "away_team_id": away_team,
                    "status": "scheduled"
                }
                create_match_resp = requests.post(f"{MANAGEMENT_BASE}/matches", json=match_payload)
                if create_match_resp.status_code in (200, 201):
                    st.success("Match created!")
                else:
                    st.error(f"Failed: {create_match_resp.text}")

    st.subheader("4. End a Match")
    with st.form("end_match"):
        match_id_to_end = st.number_input("Match ID to end", min_value=1, step=1)
    if st.form_submit_button("End Match"):
        end_resp = requests.patch(f"{MANAGEMENT_BASE}/matches/{match_id_to_end}/end")
        if end_resp.status_code == 200:
            st.success("Match ended!")
        elif end_resp.status_code == 404:
            st.error("Match not found.")
        else:
            st.error(f"Failed: {end_resp.text}")
            
    st.subheader("Delete a League")
    with st.form("delete_league"):
        league_id_to_delete = st.number_input("League ID to delete", min_value=1, step=1)
        delete_submitted = st.form_submit_button("Delete League")
        if delete_submitted:
            delete_resp = requests.delete(f"{MANAGEMENT_BASE}/leagues/{league_id_to_delete}")
            if delete_resp.status_code == 204:
                st.success("League deleted!")
            elif delete_resp.status_code == 404:
                st.error("League not found.")
            else:
                st.error(f"Failed to delete league: {delete_resp.text}")
    st.subheader("Delete a Team")
    with st.form("delete_team"):
        team_id_to_delete = st.number_input("Team ID to delete", min_value=1, step=1, key="delete_team")
        if st.form_submit_button("Delete Team"):
            delete_resp = requests.delete(f"{MANAGEMENT_BASE}/teams/{team_id_to_delete}")
            if delete_resp.status_code == 204:
                st.success("Team deleted!")
            elif delete_resp.status_code == 404:
                st.error("Team not found.")
            else:
                st.error(f"Failed to delete team: {delete_resp.text}")
    st.subheader("Delete a Match")
    with st.form("delete_match"):
        match_id_to_delete = st.number_input("Match ID to delete", min_value=1, step=1, key="delete_match")
        if st.form_submit_button("Delete Match"):
            delete_resp = requests.delete(f"{MANAGEMENT_BASE}/matches/{match_id_to_delete}")
            if delete_resp.status_code == 204:
                st.success("Match deleted!")
            elif delete_resp.status_code == 404:
                st.error("Match not found.")
            else:
                st.error(f"Failed to delete match: {delete_resp.text}")
# -------------------------------------------------------------------
# Scoreboard Page
# -------------------------------------------------------------------
elif page == "Scoreboard":
    st.title("Scoreboard Service")

    # 1. Get an existing match to update
    st.subheader("Update a match's score")

    match_id = st.number_input("Match ID", min_value=1, step=1)
    team_id  = st.number_input("Scoring Team ID", min_value=1, step=1)
    points_scored = st.number_input("Points scored", min_value=1, step=1)

    if st.button("Post Score Update"):
        payload = {
            "match_id": match_id,
            "team_id": team_id,
            "points_scored": points_scored
        }
        score_update_resp = requests.post(f"{SCOREBOARD_BASE}/score/update", json=payload)
        if score_update_resp.status_code == 200:
            st.success(f"Score updated: {score_update_resp.json()}")
        else:
            st.error(f"Failed to update score: {score_update_resp.text}")

    st.subheader("Get Live Score")
    match_id_for_score = st.number_input("Enter Match ID to retrieve score", min_value=1, step=1, key="score_match_id")
    if st.button("Fetch Score"):
        live_score_resp = requests.get(f"{SCOREBOARD_BASE}/score/{match_id_for_score}")
        if live_score_resp.status_code == 200:
            data = live_score_resp.json()
            st.write("Current Score:", data)
        else:
            st.error(f"Failed to fetch score: {live_score_resp.text}")

# -------------------------------------------------------------------
# Analytics Page
# -------------------------------------------------------------------
elif page == "Analytics":
    st.title("Analytics Service")

    st.subheader("League Standings")

    league_id_input = st.number_input("League ID", min_value=1, step=1, key="analytics_league_id")

    if st.button("Get Standings"):
        url = f"{ANALYTICS_BASE}/analytics/standings/{league_id_input}"
        resp = requests.get(url)
        if resp.status_code == 200:
            standings_data = resp.json()
            st.json(standings_data)
        else:
            st.error(f"Failed to get standings: {resp.text}")
