from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_full_match_round_event_statistics_analysis_workflow():
    # 1. Create match
    match_response = client.post(
        "/matches",
        json={
            "title": "Automated Test Match",
            "map_name": "Ascent",
            "player_agent": "Jett",
            "rank": "Gold 2",
        },
    )

    assert match_response.status_code == 201

    match_data = match_response.json()
    match_id = match_data["id"]

    assert match_data["title"] == "Automated Test Match"
    assert match_data["map_name"] == "Ascent"

    # 2. Create round 1
    round_1_response = client.post(
        f"/matches/{match_id}/rounds",
        json={
            "round_number": 1,
            "side": "attack",
            "round_result": "lost",
            "spike_planted": False,
            "site": None,
            "start_time_seconds": 0,
            "end_time_seconds": 95,
        },
    )

    assert round_1_response.status_code == 201
    round_1_id = round_1_response.json()["id"]

    # 3. Create round 2
    round_2_response = client.post(
        f"/matches/{match_id}/rounds",
        json={
            "round_number": 2,
            "side": "attack",
            "round_result": "lost",
            "spike_planted": True,
            "site": "A",
            "start_time_seconds": 96,
            "end_time_seconds": 190,
        },
    )

    assert round_2_response.status_code == 201
    round_2_id = round_2_response.json()["id"]

    # 4. Create round 3
    round_3_response = client.post(
        f"/matches/{match_id}/rounds",
        json={
            "round_number": 3,
            "side": "defense",
            "round_result": "won",
            "spike_planted": False,
            "site": None,
            "start_time_seconds": 191,
            "end_time_seconds": 280,
        },
    )

    assert round_3_response.status_code == 201
    round_3_id = round_3_response.json()["id"]

    # 5. Add first_death event in round 1
    event_1_response = client.post(
        f"/rounds/{round_1_id}/events",
        json={
            "timestamp_seconds": 32,
            "event_type": "first_death",
            "actor": "self",
            "target": None,
            "location": "mid",
            "description": "Player died first while peeking mid without trade support.",
            "source": "manual",
            "confidence": 1.0,
        },
    )

    assert event_1_response.status_code == 201

    # 6. Add first_death event in round 2
    event_2_response = client.post(
        f"/rounds/{round_2_id}/events",
        json={
            "timestamp_seconds": 30,
            "event_type": "first_death",
            "actor": "self",
            "target": None,
            "location": "A main",
            "description": "Player died first while entering A main.",
            "source": "manual",
            "confidence": 1.0,
        },
    )

    assert event_2_response.status_code == 201

    # 7. Add utility_unused event in round 2
    event_3_response = client.post(
        f"/rounds/{round_2_id}/events",
        json={
            "timestamp_seconds": 74,
            "event_type": "utility_unused",
            "actor": "self",
            "target": None,
            "location": "A site",
            "description": "Player died after spike plant with dash and smoke still available.",
            "source": "manual",
            "confidence": 1.0,
        },
    )

    assert event_3_response.status_code == 201

    # 8. Add trade_kill event in round 3
    event_4_response = client.post(
        f"/rounds/{round_3_id}/events",
        json={
            "timestamp_seconds": 44,
            "event_type": "trade_kill",
            "actor": "teammate",
            "target": "enemy",
            "location": "B main",
            "description": "Teammate traded the first contact quickly.",
            "source": "manual",
            "confidence": 1.0,
        },
    )

    assert event_4_response.status_code == 201

    # 9. Get statistics
    statistics_response = client.get(f"/matches/{match_id}/statistics")

    assert statistics_response.status_code == 200

    statistics = statistics_response.json()

    assert statistics["match_id"] == match_id
    assert statistics["total_rounds"] == 3
    assert statistics["rounds_won"] == 1
    assert statistics["rounds_lost"] == 2
    assert statistics["spike_plants"] == 1
    assert statistics["post_plant_losses"] == 1
    assert statistics["first_death_count"] == 2
    assert statistics["utility_unused_count"] == 1
    assert statistics["trade_kill_count"] == 1

    # 10. Run and save analysis
    analysis_response = client.post(f"/matches/{match_id}/analyze")

    assert analysis_response.status_code == 200

    analysis = analysis_response.json()

    assert analysis["match_id"] == match_id
    assert analysis["total_findings"] >= 1

    issue_types = [finding["issue_type"] for finding in analysis["findings"]]

    assert "early_round_risk" in issue_types
    assert "post_plant_conversion_issue" in issue_types
    assert "utility_unused_in_lost_round" in issue_types

    # 11. Retrieve saved analysis
    saved_analysis_response = client.get(f"/matches/{match_id}/analysis")

    assert saved_analysis_response.status_code == 200

    saved_analysis = saved_analysis_response.json()

    assert saved_analysis["match_id"] == match_id
    assert saved_analysis["total_findings"] == analysis["total_findings"]


def test_missing_match_statistics_returns_404():
    response = client.get("/matches/999999/statistics")

    assert response.status_code == 404
    assert response.json()["detail"] == "Match with id 999999 not found"


def test_missing_match_analysis_returns_404():
    response = client.post("/matches/999999/analyze")

    assert response.status_code == 404
    assert response.json()["detail"] == "Match with id 999999 not found"


def test_missing_saved_analysis_returns_404():
    response = client.get("/matches/999999/analysis")

    assert response.status_code == 404
    assert response.json()["detail"] == "Match with id 999999 not found"