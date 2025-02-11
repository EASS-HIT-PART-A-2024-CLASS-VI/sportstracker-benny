# analytics_service/routers/analytics.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Match, Team
from .. import schemas

router = APIRouter()

@router.get("/standings/{league_id}", response_model=schemas.StandingsResponse)
def get_standings(league_id: int, db: Session = Depends(get_db)):
    # 1. Get all "finished" matches for this league
    finished_matches = db.query(Match).filter(
        Match.league_id == league_id,
        Match.status == "finished"
    ).all()

    # 2. Build a dict of team_id -> stats
    team_stats = {}

    # Gather all teams in this league
    league_teams = db.query(Team).filter(Team.league_id == league_id).all()
    if not league_teams:
        raise HTTPException(status_code=404, detail="No teams found for this league")

    for t in league_teams:
        team_stats[t.id] = {
            "team_id": t.id,
            "name": t.name,
            "points": 0,
            "wins": 0,
            "draws": 0,
            "losses": 0
        }

    # 3. Iterate over finished matches
    for match in finished_matches:
        home = team_stats.get(match.home_team_id)
        away = team_stats.get(match.away_team_id)
        if not home or not away:
            # Should not happen, but just in case
            continue
        
        if match.home_score > match.away_score:#a win is worth 3 points, a draw is worth 1 point (to each team), and a loss is worth 0 points
            home["wins"] += 1
            home["points"] += 3
            away["losses"] += 1
        elif match.home_score < match.away_score:
            away["wins"] += 1
            away["points"] += 3
            home["losses"] += 1
        else:
            # draw
            home["draws"] += 1
            home["points"] += 1
            away["draws"] += 1
            away["points"] += 1

    # 4. Sort by points descending
    sorted_standings = sorted(team_stats.values(), key=lambda x: x["points"], reverse=True)

    return {
        "league_id": league_id,
        "standings": sorted_standings
    }
