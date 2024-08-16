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
