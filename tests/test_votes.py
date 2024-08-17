def test_vote_on_post_unauth(client):
    post_id = 1
    resp = client.post(
        "/vote/", json={"post_id": post_id, "vote_direction": 1}
    )
    print(resp.json())
    assert resp.status_code == 401


def test_vote_on_non_exist_post(auth_client):
    resp = auth_client.post(
        "/vote/", json={"post_id": 1, "vote_direction": 1}
    )
    print(resp.json())
    assert resp.status_code == 404


def test_vote_on_post_wrong_direction(auth_client):
    resp = auth_client.post(
        "/vote/", json={"post_id": 1, "vote_direction": 0}
    )
    print(resp.json())
    assert resp.status_code == 422


def test_vote_on_post_vote_up(auth_client, create_posts):
    post_id = 1
    resp = auth_client.post(
        "/vote/", json={"post_id": post_id, "vote_direction": 1}
    )
    print(resp.json())
    assert resp.status_code == 201

    resp = auth_client.post(
        "/vote/", json={"post_id": post_id, "vote_direction": 1}
    )
    print(resp.json())
    assert resp.status_code == 400
    if f"User with id" in resp.json()["detail"]:
        assert True


def test_vote_on_post_vote_down(auth_client, create_posts):
    post_id = 1
    resp = auth_client.post(
        "/vote/", json={"post_id": post_id, "vote_direction": -1}
    )
    print(resp.json())
    assert resp.status_code == 400
    if "User with id" in resp.json()["detail"] and "did not voted" in resp.json()["detail"]:
        assert True

    resp = auth_client.post(
        "/vote/", json={"post_id": post_id, "vote_direction": 1}
    )
    print(resp.json())
    assert resp.status_code == 201

    resp = auth_client.post(
        "/vote/", json={"post_id": post_id, "vote_direction": -1}
    )
    print(resp.json())
    assert resp.status_code == 201
    if "Post with id" not in resp.json()["message"] or  "has been un-voted" not in resp.json()["message"]:
        assert False
