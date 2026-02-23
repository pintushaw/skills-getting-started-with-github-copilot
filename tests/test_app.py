from src.app import activities


def test_root_redirects_to_static_index(client):
    response = client.get("/", follow_redirects=False)

    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


def test_get_activities_returns_activity_map(client):
    response = client.get("/activities")

    payload = response.json()

    assert response.status_code == 200
    assert isinstance(payload, dict)
    assert "Chess Club" in payload


def test_signup_adds_participant_successfully(client):
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"

    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    payload = response.json()

    assert response.status_code == 200
    assert payload["message"] == f"Signed up {email} for {activity_name}"
    assert email in activities[activity_name]["participants"]


def test_signup_returns_404_for_unknown_activity(client):
    response = client.post("/activities/Unknown%20Club/signup", params={"email": "student@mergington.edu"})

    payload = response.json()

    assert response.status_code == 404
    assert payload["detail"] == "Activity not found"


def test_signup_returns_400_for_duplicate_participant(client):
    activity_name = "Chess Club"
    email = activities[activity_name]["participants"][0]

    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    payload = response.json()

    assert response.status_code == 400
    assert payload["detail"] == "Student already signed up for this activity"


def test_signup_returns_422_when_email_missing(client):
    response = client.post("/activities/Chess%20Club/signup")

    assert response.status_code == 422


def test_unregister_removes_participant_successfully(client):
    activity_name = "Chess Club"
    email = activities[activity_name]["participants"][0]

    response = client.delete(f"/activities/{activity_name}/unregister", params={"email": email})

    payload = response.json()

    assert response.status_code == 200
    assert payload["message"] == f"Unregistered {email} from {activity_name}"
    assert email not in activities[activity_name]["participants"]


def test_unregister_returns_404_for_unknown_activity(client):
    response = client.delete("/activities/Unknown%20Club/unregister", params={"email": "student@mergington.edu"})

    payload = response.json()

    assert response.status_code == 404
    assert payload["detail"] == "Activity not found"


def test_unregister_returns_404_when_participant_not_registered(client):
    response = client.delete(
        "/activities/Chess%20Club/unregister",
        params={"email": "notregistered@mergington.edu"},
    )

    payload = response.json()

    assert response.status_code == 404
    assert payload["detail"] == "Student not registered for this activity"


def test_unregister_returns_422_when_email_missing(client):
    response = client.delete("/activities/Chess%20Club/unregister")

    assert response.status_code == 422