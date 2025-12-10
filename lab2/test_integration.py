import pytest
from httpx import AsyncClient
from asgi_lifespan import LifespanManager
from app.main import app

@pytest.mark.asyncio
async def test_register_user():
    async with LifespanManager(app): 
        async with AsyncClient(base_url="http://test", app=app) as ac:
            response = await ac.post("/api/users", json={
                "user": {
                    "username": "testuser",
                    "email": "testuser@example.com",
                    "password": "password123"
                }
            })
            assert response.status_code == 201
            data = response.json()
            assert data["user"]["username"] == "testuser"
            assert data["user"]["email"] == "testuser@example.com"

@pytest.mark.anyio
async def test_login_user():
    async with LifespanManager(app):
        async with AsyncClient(app=app, base_url="http://test") as ac:

            await ac.post("/api/users", json={
                "user": {
                    "username": "testlogin",
                    "email": "login@example.com",
                    "password": "password123"
                }
            })

            response = await ac.post("/api/users/login", json={
                "user": {
                    "email": "login@example.com",
                    "password": "password123"
                }
            })
            assert response.status_code == 200
            data = response.json()
            assert "token" in data["user"]

@pytest.mark.anyio
async def test_create_article():
    async with LifespanManager(app):
        async with AsyncClient(app=app, base_url="http://test") as ac:

            await ac.post("/api/users", json={
                "user": {"username": "author", "email": "author@example.com", "password": "password123"}
            })
            login_resp = await ac.post("/api/users/login", json={
                "user": {"email": "author@example.com", "password": "password123"}
            })
            token = login_resp.json()["user"]["token"]

            response = await ac.post(
                "/api/articles",
                json={
                    "article": {"title": "Test Article", "description": "Desc", "body": "Content"}
                },
                headers={"Authorization": f"Token {token}"}
            )
            assert response.status_code == 201
            data = response.json()
            assert data["article"]["title"] == "Test Article"

@pytest.mark.anyio
async def test_feed():
    async with LifespanManager(app):
        async with AsyncClient(app=app, base_url="http://test") as ac:

            await ac.post("/api/users", json={"user": {"username": "feeduser", "email": "feed@example.com", "password": "password123"}})
            login_resp = await ac.post("/api/users/login", json={"user": {"email": "feed@example.com", "password": "password123"}})
            token = login_resp.json()["user"]["token"]

            response = await ac.get("/api/articles/feed", headers={"Authorization": f"Token {token}"})
            assert response.status_code == 200
            assert "articles" in response.json()

@pytest.mark.anyio
async def test_favorite_article():
    async with LifespanManager(app):
        async with AsyncClient(app=app, base_url="http://test") as ac:

            await ac.post("/api/users", json={"user": {"username": "favuser", "email": "fav@example.com", "password": "password123"}})
            login_resp = await ac.post("/api/users/login", json={"user": {"email": "fav@example.com", "password": "password123"}})
            token = login_resp.json()["user"]["token"]

            create_resp = await ac.post(
                "/api/articles",
                json={"article": {"title": "Fav Article", "description": "Desc", "body": "Content"}},
                headers={"Authorization": f"Token {token}"}
            )
            slug = create_resp.json()["article"]["slug"]

            fav_resp = await ac.post(f"/api/articles/{slug}/favorite", headers={"Authorization": f"Token {token}"})
            assert fav_resp.status_code == 200
            assert fav_resp.json()["article"]["favorited"] is True
