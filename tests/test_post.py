from app import schemas
import pytest


def test_get_all_posts(client, create_posts):
    resp = client.get("/posts/")
    # print(resp.json())

    # def convert(post):
    #     return schemas.PostVoteOut(**post)
    # posts_map = map(convert, resp.json())
    # print(list(posts_map))

    posts = [schemas.PostVoteOut(**post) for post in resp.json()]

    assert resp.status_code == 200
    assert len(posts) == create_posts


@pytest.mark.parametrize("title,content,published", [
    ("test1", "test1", True),
    ("test2", "test2", False),
    ("test3", "test3", True),
])
def test_create_posts(auth_client, title, content, published):
    post = {"title": title, "content": content, "published": published}
    resp = auth_client.post(
        "/posts/", json=post
    )
    print(resp.json())
    assert resp.status_code == 201
    post_resp = schemas.PostResponse(**resp.json())
    assert post_resp.title == title


@pytest.mark.parametrize("title,content", [
    ("test1", "test1"),
    ("test2", "test2"),
    ("test3", "test3"),
])
def test_create_posts_default(auth_client, title, content):
    post = {"title": title, "content": content}
    resp = auth_client.post(
        "/posts/", json=post
    )
    print(resp.json())
    assert resp.status_code == 201
    post_resp = schemas.PostResponse(**resp.json())
    assert post_resp.title == title
    assert post_resp.published == True


def test_create_posts_unauthorized(client):
    post = {"title": "test1", "content": "test1", "published": True}
    resp = client.post(
        "/posts/", json=post
    )
    print(resp.json())
    assert resp.status_code == 401


def test_get_one_non_exist_post(client):
    resp = client.get("/posts/100")
    assert resp.status_code == 404


def test_get_one_post(client, create_posts):
    resp = client.get("/posts/1")
    print(resp.json())
    post = schemas.PostVoteOut(**resp.json())
    print("*************", post)
    assert resp.status_code == 200
    assert post.Posts.id == 1
    assert post.Posts.user.id == 1


def test_delete_post_unauthorized(client):
    resp = client.delete("/posts/100")
    assert resp.status_code == 401


def test_delete_post_authorized(auth_client, create_posts):
    resp = auth_client.delete("/posts/1")
    assert resp.status_code == 204


def test_update_posts(auth_client, create_posts):
    new_title = "title11"
    new_content = "content11"
    post = {"title": new_title, "content": new_content}
    resp = auth_client.put(
        "/posts/1", json=post
    )
    print(resp.json())
    assert resp.status_code == 200
    post_resp = schemas.PostResponse(**resp.json())
    assert post_resp.title == new_title
    assert post_resp.content == new_content


def test_update_posts_unauth(client):
    new_title = "title11"
    new_content = "content11"
    post = {"title": new_title, "content": new_content}
    resp = client.put(
        "/posts/1", json=post
    )
    print(resp.json())
    assert resp.status_code == 401


def test_update_posts_non_exist(auth_client, create_posts):
    id = 10
    new_title = "title11"
    new_content = "content11"
    post = {"title": new_title, "content": new_content}
    resp = auth_client.put(
        f"/posts/{id}", json=post
    )
    print(resp.json())
    assert resp.status_code == 404
    assert resp.json()["detail"] == f"Post with id: {id} not found"

def test_update_posts_user_not_allowed(create_posts, auth_client2):
    id = 1
    new_title = "title11"
    new_content = "content11"
    post = {"title": new_title, "content": new_content}
    resp = auth_client2.put(
        f"/posts/{id}", json=post
    )
    print(resp.json())
    assert resp.status_code == 403
    assert resp.json()["detail"] == "You are not allowed to update this post"