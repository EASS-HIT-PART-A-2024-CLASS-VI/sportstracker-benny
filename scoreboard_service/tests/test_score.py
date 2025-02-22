import pytest
import httpx

@pytest.fixture(scope="session")
def scoreboard_client():
    return httpx.Client(base_url="http://scoreboard_service:8000")
def management_client():
    return httpx.Client(base_url="http://management_service:8000")

def test_score_update_flow(management_client, scoreboard_client):
    # 1. Create a league 
    league_payload = {"name": "ScoreTest", "country": "TestLand"}
    league_resp = management_client.post("/leagues/", json=league_payload)
    assert league_resp.status_code in (200, 201), f"Create league failed: {league_resp.text}"
    league_id = league_resp.json()["id"]

    # 2. Create two teams
    team1_payload = {"name": "TeamA", "city": "CityA", "league_id": league_id}
    team2_payload = {"name": "TeamB", "city": "CityB", "league_id": league_id}

    team1_resp = management_client.post("/teams/", json=team1_payload)
    team2_resp = management_client.post("/teams/", json=team2_payload)
    assert team1_resp.status_code in (200, 201), f"Create team1 failed: {team1_resp.text}"
    assert team2_resp.status_code in (200, 201), f"Create team2 failed: {team2_resp.text}"
    team1_id = team1_resp.json()["id"]
    team2_id = team2_resp.json()["id"]

    # 3. Create a match
    match_payload = {
        "league_id": league_id,
        "home_team_id": team1_id,
        "away_team_id": team2_id,
        "status": "scheduled"
    }
    match_resp = management_client.post("/matches/", json=match_payload)
    assert match_resp.status_code in (200, 201), f"Create match failed: {match_resp.text}"
    match_id = match_resp.json()["id"]

    # 4. Update the match using scoreboard service
    score_update_payload = {
        "match_id": match_id,
        "team_id": team1_id,
        "points_scored": 3
    }
    score_resp = scoreboard_client.post("/score/update", json=score_update_payload)
    assert score_resp.status_code == 200, f"Score update failed: {score_resp.text}"
    updated_score = score_resp.json()
    assert updated_score["home_score"] == 3, "Expected home_score to be 3"

    # 5. Fetch the live score
    get_score_resp = scoreboard_client.get(f"/score/{match_id}")
    assert get_score_resp.status_code == 200, f"Get score failed: {get_score_resp.text}"
    live_data = get_score_resp.json()
    assert live_data["home_score"] == 3, "Expected home_score to be 3"

    print("Scoreboard cross-service test completed!")