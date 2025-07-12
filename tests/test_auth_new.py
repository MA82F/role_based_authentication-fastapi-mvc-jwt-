import pytest
from httpx import AsyncClient


class TestAuthModule:
    """Test cases for authentication module"""

    @pytest.mark.asyncio
    async def test_signup_success(self, client: AsyncClient):
        """Test successful user signup"""
        user_data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "password123",
        }

        response = await client.post("/auth/signup", json=user_data)

        assert response.status_code == 201
        data = response.json()
        assert data["username"] == user_data["username"]
        assert data["email"] == user_data["email"]
        assert data["role"] == "user"  # Default role
        assert data["is_active"] is True
        assert "id" in data
        assert "created_at" in data
        assert "password" not in data  # Password should not be returned

    @pytest.mark.asyncio
    async def test_signup_duplicate_username(self, client: AsyncClient):
        """Test signup with duplicate username"""
        user_data = {
            "username": "duplicate",
            "email": "first@example.com",
            "password": "password123",
        }

        # First signup
        response1 = await client.post("/auth/signup", json=user_data)
        assert response1.status_code == 201

        # Second signup with same username
        user_data["email"] = "second@example.com"
        response2 = await client.post("/auth/signup", json=user_data)
        assert response2.status_code == 400

    @pytest.mark.asyncio
    async def test_signup_duplicate_email(self, client: AsyncClient):
        """Test signup with duplicate email"""
        user_data = {
            "username": "user1",
            "email": "duplicate@example.com",
            "password": "password123",
        }

        # First signup
        response1 = await client.post("/auth/signup", json=user_data)
        assert response1.status_code == 201

        # Second signup with same email
        user_data["username"] = "user2"
        response2 = await client.post("/auth/signup", json=user_data)
        assert response2.status_code == 400

    @pytest.mark.asyncio
    async def test_signup_invalid_email(self, client: AsyncClient):
        """Test signup with invalid email format"""
        user_data = {
            "username": "testuser",
            "email": "invalid-email",
            "password": "password123",
        }

        response = await client.post("/auth/signup", json=user_data)
        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_login_success(self, client: AsyncClient, test_user_data):
        """Test successful login"""
        # First create user
        await client.post("/auth/signup", json=test_user_data)

        # Then login
        login_data = {
            "username": test_user_data["username"],
            "password": test_user_data["password"],
        }

        response = await client.post("/auth/login", json=login_data)

        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert isinstance(data["access_token"], str)
        assert len(data["access_token"]) > 0

    @pytest.mark.asyncio
    async def test_login_wrong_username(self, client: AsyncClient, test_user_data):
        """Test login with wrong username"""
        # Create user
        await client.post("/auth/signup", json=test_user_data)

        # Try login with wrong username
        login_data = {"username": "wronguser", "password": test_user_data["password"]}

        response = await client.post("/auth/login", json=login_data)
        assert response.status_code == 401

    @pytest.mark.asyncio
    async def test_login_wrong_password(self, client: AsyncClient, test_user_data):
        """Test login with wrong password"""
        # Create user
        await client.post("/auth/signup", json=test_user_data)

        # Try login with wrong password
        login_data = {
            "username": test_user_data["username"],
            "password": "wrongpassword",
        }

        response = await client.post("/auth/login", json=login_data)
        assert response.status_code == 401

    @pytest.mark.asyncio
    async def test_login_missing_fields(self, client: AsyncClient):
        """Test login with missing fields"""
        # Missing password
        response1 = await client.post("/auth/login", json={"username": "test"})
        assert response1.status_code == 422

        # Missing username
        response2 = await client.post("/auth/login", json={"password": "test"})
        assert response2.status_code == 422

        # Empty body
        response3 = await client.post("/auth/login", json={})
        assert response3.status_code == 422
