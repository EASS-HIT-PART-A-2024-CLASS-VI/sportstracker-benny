import pytest
import httpx

@pytest.fixture(scope="session")
def services():
    return {
        "management": httpx.Client(base_url="http://management_service:8000"),
        "scoreboard": httpx.Client(base_url="http://scoreboard_service:8000"),
        "analytics": httpx.Client(base_url="http://analytics_service:8000")
    }

def test_end_to_end(services):
    management = services["management"]
    scoreboard = services["scoreboard"]
    analytics = services["analytics"]

    # 1. Register a new user
    user_payload = {"username": "e2e_user", "password": "test_pass"}
    reg_resp = management.post("/register", json=user_payload)
    assert reg_resp.status_code in (200, 201), f"Register failed: {reg_resp.text}"
    created_user = reg_resp.json()
    assert created_user["username"] == "e2e_user"

    # 2. Create a league
    league_payload = {"name": "E2E League", "country": "TestLand"}
    league_resp = management.post("/leagues", json=league_payload)
    assert league_resp.status_code in (200, 201), f"Create league failed: {league_resp.text}"
    created_league = league_resp.json()
    league_id = created_league["id"]

    # 3. Create a team
    team_payload = {
        "name": "E2E Team",
        "city": "TestCity",
        "league_id": league_id
    }
    team_resp = management.post("/teams", json=team_payload)
    assert team_resp.status_code in (200, 201), f"Create team failed: {team_resp.text}"
    created_team = team_resp.json()
    team_id = created_team["id"]

    # 4. Create a match
    match_payload = {
        "league_id": league_id,
        "home_team_id": team_id,
        "away_team_id": team_id,  
        "status": "scheduled"
    }
    match_resp = management.post("/matches", json=match_payload)
    assert match_resp.status_code in (200, 201), f"Create match failed: {match_resp.text}"
    created_match = match_resp.json()
    match_id = created_match["id"]

    # 5. Update (score) the match - scoreboard_service
    score_update_payload = {
        "match_id": match_id,
        "team_id": team_id,
        "points_scored": 3
    }
    score_resp = scoreboard.post("/score/update", json=score_update_payload)
    assert score_resp.status_code == 200, f"Score update failed: {score_resp.text}"

    # 6. End the match (finish it)
    end_resp = management.patch(f"/matches/{match_id}/end")
    assert end_resp.status_code == 200, f"End match failed: {end_resp.text}"
    ended_info = end_resp.json()
    assert ended_info["status"] == "finished", "Match should now be finished."

    # 7. Fetch analytics
    standings_resp = analytics.get(f"/analytics/standings/{league_id}")
    assert standings_resp.status_code == 200, f"Analytics failed: {standings_resp.text}"
    standings = standings_resp.json()
    # Check that we got back a 'standings' array
    assert "standings" in standings, f"Missing 'standings' in analytics response: {standings}"
    assert len(standings["standings"]) > 0, "Expected at least one team in standings."

    print("E2E test completed successfully!")
