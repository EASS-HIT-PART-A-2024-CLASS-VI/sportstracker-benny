import pytest
import httpx
import time

@pytest.fixture(scope="session")
def management_client():
    return httpx.Client(base_url="http://management_service:8000")

@pytest.fixture(scope="session")
def scoreboard_client():
    return httpx.Client(base_url="http://scoreboard_service:8000")

@pytest.fixture(scope="session")
def analytics_client():
    return httpx.Client(base_url="http://analytics_service:8000")

def test_analytics_standings_flow(management_client, scoreboard_client, analytics_client):
    # 1. Create a league
    league_payload = {"name": "AnalyticsTest", "country": "TestLand"}
    league_resp = management_client.post("/leagues/", json=league_payload)
    assert league_resp.status_code in (200, 201), f"Create league failed: {league_resp.text}"
    league_id = league_resp.json()["id"]

    # 2. Create two teams
    team1_payload = {"name": "AnalyticsTeamA", "city": "CityA", "league_id": league_id}
    team2_payload = {"name": "AnalyticsTeamB", "city": "CityB", "league_id": league_id}

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

    # 4. Update (score) the match using scoreboard_service
    score_update_payload = {
        "match_id": match_id,
        "team_id": team1_id,
        "points_scored": 5
    }
    score_resp = scoreboard_client.post("/score/update", json=score_update_payload)
    assert score_resp.status_code == 200, f"Score update failed: {score_resp.text}"

    # 5. End the match
    end_resp = management_client.patch(f"/matches/{match_id}/end")
    assert end_resp.status_code == 200, f"End match failed: {end_resp.text}"
    ended_info = end_resp.json()
    assert ended_info["status"] == "finished", "Match should be finished."

    # 6. Fetch standings from analytics_service
    standings_resp = analytics_client.get(f"/analytics/standings/{league_id}")
    assert standings_resp.status_code == 200, f"Get standings failed: {standings_resp.text}"
    standings_data = standings_resp.json()

    # Basic check that we have a 'standings' list
    assert "standings" in standings_data, "Expected a 'standings' key in the response"
    print("Analytics integration test completed successfully!")
