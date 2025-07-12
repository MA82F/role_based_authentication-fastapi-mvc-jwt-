import pytest


class TestJWTProtectedRoutes:
    """Test JWT authentication and protected routes"""

    @pytest.mark.asyncio
    async def test_protected_route_without_token(self, client):
        """Test accessing protected route without token"""
        async with client as c:
            response = await c.get("/user/profile")
            assert response.status_code == 403

    @pytest.mark.asyncio
    async def test_protected_route_with_invalid_token(self, client):
        """Test accessing protected route with invalid token"""
        headers = {"Authorization": "Bearer invalid_token"}
        async with client as c:
            response = await c.get("/user/profile", headers=headers)
            assert response.status_code == 401

    @pytest.mark.asyncio 
    async def test_protected_route_with_valid_token(self, client, authenticated_user, test_user_data):
        """Test accessing protected route with valid JWT token"""
        async with client as c:
            # Get authenticated headers
            headers = await authenticated_user(c, test_user_data)
            
            response = await c.get("/user/profile", headers=headers)
            assert response.status_code == 200
            data = response.json()
            assert "username" in data
            assert "email" in data
            assert "id" in data
