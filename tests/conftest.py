from fastapi.testclient import TestClient
from app.main_sa import app
from app.config import settings
from app.database import get_db, Base
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import pytest
from app.outh2 import create_access_token
import jwt

# postgresql+psycopg: means which postgres driver to use if omitted like (postgresql://) then by default it will use psycopg2
test_db_url = f"{settings.database_url}_test"
test_db_url = "postgresql+psycopg://postgres:postgres@localhost:5432/fastapi_test"
# print(test_db_url)
SQLALCHEMY_DATABASE_URL = test_db_url  # settings.database_url

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client(session):
    def get_test_db():
        try:
            yield session
        finally:
            session.close()

    # Dependency Injection
    app.dependency_overrides[get_db] = get_test_db
    yield TestClient(app)


@pytest.fixture
def test_user(client):
    user = {
        "email": "test1@gmail.com",
        "password": "password"
    }
    response = client.post("/users/", json=user)
    print(response.json())
    assert response.status_code == 201
    new_user = response.json()
    new_user["password"] = user["password"]
    return new_user


@pytest.fixture
def token(test_user):
    return create_access_token(data={"user_id": test_user["id"]})


@pytest.fixture
def auth_client(client, token):
    client.headers = {**client.headers, "Authorization": f"Bearer {token}"}
    return client


@pytest.fixture
def create_posts(auth_client):
    posts=[
        {"title": "test1", "content": "test1", "published": True},
        {"title": "test2", "content": "test2", "published": False},
        {"title": "test3", "content": "test3", "published": True},
    ]
    for post in posts:
        resp = auth_client.post(
            "/posts/", json=post
        )
        assert resp.status_code == 201
    return len(posts)
