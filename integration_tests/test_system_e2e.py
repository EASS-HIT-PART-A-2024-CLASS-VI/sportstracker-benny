# integration_tests/test_system_e2e.py

import time
import pytest


def test_full_system_flow(management_client, scoreboard_client, analytics_client):
    # 1. Register user
    unique_username = f"sys_user_{int(time.time())}"
    user_payload = {"username": unique_username, "password": "test_pass"}
    reg_resp = management_client.post("/register", json=user_payload)
    assert reg_resp.status_code in (200, 201), f"Register user failed: {reg_resp.text}"

    # 2. Create league
    league_payload = {"name": "SystemTestLeague", "country": "SystemLand"}
    league_resp = management_client.post("/leagues/", json=league_payload)
    assert league_resp.status_code in (200, 201), f"Create league failed: {league_resp.text}"
    league_id = league_resp.json()["id"]

    # 3. Create 2 teams
    team1_payload = {"name": "SystemTeamA", "city": "SysCityA", "league_id": league_id}
    team2_payload = {"name": "SystemTeamB", "city": "SysCityB", "league_id": league_id}

    team1_resp = management_client.post("/teams/", json=team1_payload)
    team2_resp = management_client.post("/teams/", json=team2_payload)
    assert team1_resp.status_code in (200, 201), f"Create team1 failed: {team1_resp.text}"
    assert team2_resp.status_code in (200, 201), f"Create team2 failed: {team2_resp.text}"
    team1_id = team1_resp.json()["id"]
    team2_id = team2_resp.json()["id"]

    # 4. Create match
    match_payload = {
        "league_id": league_id,
        "home_team_id": team1_id,
        "away_team_id": team2_id,
        "status": "scheduled"
    }
    match_resp = management_client.post("/matches/", json=match_payload)
    assert match_resp.status_code in (200, 201), f"Create match failed: {match_resp.text}"
    match_id = match_resp.json()["id"]

    # 5. Update score via scoreboard_service
    score_update_payload = {
        "match_id": match_id,
        "team_id": team1_id,
        "points_scored": 2
    }
    score_resp = scoreboard_client.post("/score/update", json=score_update_payload)
    assert score_resp.status_code == 200, f"Score update failed: {score_resp.text}"

    # 6. End the match in management_service
    end_resp = management_client.patch(f"/matches/{match_id}/end")
    assert end_resp.status_code == 200, f"End match failed: {end_resp.text}"

    # 7. Check standings in analytics_service
    standings_resp = analytics_client.get(f"/analytics/standings/{league_id}")
    assert standings_resp.status_code == 200, f"Standings fetch failed: {standings_resp.text}"
    standings_data = standings_resp.json()
    assert "standings" in standings_data, "Expected 'standings' key in analytics response"

    print("System E2E test completed successfully!")
