import pytest
import requests
import time

BASE_MANAGEMENT = "http://localhost:8000"
BASE_SCOREBOARD = "http://localhost:8001"
BASE_ANALYTICS = "http://localhost:8002"

def test_end_to_end():
    # 1. Create league
    league_resp = requests.post(f"{BASE_MANAGEMENT}/leagues", json={"name": "Premier League"})
    assert league_resp.status_code == 200
    league_id = league_resp.json()["id"]

    # 2. Create two teams
    team_a_resp = requests.post(f"{BASE_MANAGEMENT}/teams", json={"name":"Team A", "city":"City A", "league_id": league_id})
    team_b_resp = requests.post(f"{BASE_MANAGEMENT}/teams", json={"name":"Team B", "city":"City B", "league_id": league_id})
    team_a_id = team_a_resp.json()["id"]
    team_b_id = team_b_resp.json()["id"]

    # 3. Create match
    match_resp = requests.post(f"{BASE_MANAGEMENT}/matches", json={
        "league_id": league_id,
        "home_team_id": team_a_id,
        "away_team_id": team_b_id,
        "status": "scheduled"
    })
    match_id = match_resp.json()["id"]

    # 4. Score updates
    sc1 = requests.post(f"{BASE_SCOREBOARD}/score/update", json={
        "match_id": match_id,
        "team_id": team_a_id,
        "points_scored": 2
    })
    assert sc1.status_code == 200

    sc2 = requests.post(f"{BASE_SCOREBOARD}/score/update", json={
        "match_id": match_id,
        "team_id": team_b_id,
        "points_scored": 1
    })
    assert sc2.status_code == 200

    # 5. Mark match as finished (fake approach or scoreboard endpoint)
    sc3 = requests.post(f"{BASE_SCOREBOARD}/score/update", json={
        "match_id": match_id,
        "team_id": 0,
        "points_scored": 0,
        "final_status": "finished"  # you'd code scoreboard to handle this
    })

    time.sleep(1)  # wait a bit for DB commits, etc.

    # 6. Check analytics
    st = requests.get(f"{BASE_ANALYTICS}/analytics/standings/{league_id}")
    assert st.status_code == 200
    data = st.json()
    # data["standings"] should have Team A with 3 points, Team B with 0, etc.
    print("Standings:", data)
