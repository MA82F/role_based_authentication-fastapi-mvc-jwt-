import pytest


class TestFeedbackModule:
    """Test feedback creation and viewing according to requirements"""

    @pytest.mark.asyncio
    async def test_feedback_creation_success(self, client, authenticated_user):
        """Test successful feedback creation by authenticated user"""
        feedback_data = {"rating": 5, "comment": "Great service!"}

        async with client as c:
            response = await c.post(
                "/feedback", json=feedback_data, headers=authenticated_user
            )

            assert response.status_code == 201
            data = response.json()
            assert data["rating"] == feedback_data["rating"]
            assert data["comment"] == feedback_data["comment"]
            assert "id" in data
            assert "user_id" in data
            assert "created_at" in data

    @pytest.mark.asyncio
    async def test_feedback_creation_requires_authentication(self, client):
        """Test that feedback creation requires authentication"""
        feedback_data = {"rating": 5, "comment": "Great service!"}

        async with client as c:
            response = await c.post("/feedback", json=feedback_data)
            assert response.status_code == 403

    @pytest.mark.asyncio
    async def test_feedback_rating_validation(self, client, authenticated_user):
        """Test feedback rating validation (1-5)"""
        async with client as c:
            # Test invalid ratings
            invalid_ratings = [0, 6, -1, 10]
            for rating in invalid_ratings:
                feedback_data = {"rating": rating, "comment": "Test comment"}
                response = await c.post(
                    "/feedback", json=feedback_data, headers=authenticated_user
                )
                assert response.status_code == 422

            # Test valid ratings
            valid_ratings = [1, 2, 3, 4, 5]
            for rating in valid_ratings:
                feedback_data = {
                    "rating": rating,
                    "comment": f"Test comment for rating {rating}",
                }
                response = await c.post(
                    "/feedback", json=feedback_data, headers=authenticated_user
                )
                assert response.status_code == 201

    @pytest.mark.asyncio
    async def test_feedback_optional_comment(self, client, authenticated_user):
        """Test that comment is optional in feedback"""
        feedback_data = {
            "rating": 4
            # No comment field
        }

        async with client as c:
            response = await c.post(
                "/feedback", json=feedback_data, headers=authenticated_user
            )

            assert response.status_code == 201
            data = response.json()
            assert data["rating"] == 4
            assert data["comment"] is None

    @pytest.mark.asyncio
    async def test_feedback_missing_rating(self, client, authenticated_user):
        """Test that rating is required"""
        feedback_data = {"comment": "Comment without rating"}

        async with client as c:
            response = await c.post(
                "/feedback", json=feedback_data, headers=authenticated_user
            )
            assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_admin_can_view_all_feedback(
        self, client, authenticated_admin, authenticated_user
    ):
        """Test that admin can view all feedback entries"""
        # Create some feedback as regular user
        feedback_data = {"rating": 4, "comment": "Admin should see this"}

        async with client as c:
            await c.post("/feedback", json=feedback_data, headers=authenticated_user)

            # Admin can view all feedback
            response = await c.get("/admin/feedback", headers=authenticated_admin)

            assert response.status_code == 200
            data = response.json()
            assert isinstance(data, list)
            if len(data) > 0:
                feedback = data[0]
                assert "rating" in feedback
                assert "comment" in feedback
                assert "username" in feedback  # Should include user info
                assert "user_id" in feedback
                assert "created_at" in feedback

    @pytest.mark.asyncio
    async def test_user_cannot_view_all_feedback(self, client, authenticated_user):
        """Test that regular users cannot view all feedback"""
        async with client as c:
            response = await c.get("/admin/feedback", headers=authenticated_user)
            assert response.status_code == 403

    @pytest.mark.asyncio
    async def test_feedback_summary_public(self, client, authenticated_user):
        """Test that feedback summary is accessible (public endpoint)"""
        # Create some feedback first
        feedback_list = [
            {"rating": 5, "comment": "Excellent"},
            {"rating": 4, "comment": "Good"},
            {"rating": 3, "comment": "Average"},
        ]

        async with client as c:
            for feedback in feedback_list:
                await c.post("/feedback", json=feedback, headers=authenticated_user)

            # Test summary endpoint
            response = await c.get("/feedback/summary", headers=authenticated_user)

            assert response.status_code == 200
            data = response.json()
            assert "total_feedback" in data
            assert "average_rating" in data
            assert data["total_feedback"] == len(feedback_list)

            # Calculate expected average
            expected_avg = sum(f["rating"] for f in feedback_list) / len(feedback_list)
            assert abs(data["average_rating"] - expected_avg) < 0.01

    @pytest.mark.asyncio
    async def test_feedback_summary_without_auth(self, client):
        """Test that feedback summary requires authentication"""
        async with client as c:
            response = await c.get("/feedback/summary")
            assert response.status_code == 403

    @pytest.mark.asyncio
    async def test_multiple_feedback_from_same_user(self, client, authenticated_user):
        """Test that same user can submit multiple feedback entries"""
        feedback_list = [
            {"rating": 5, "comment": "First feedback"},
            {"rating": 3, "comment": "Second feedback"},
            {"rating": 4, "comment": "Third feedback"},
        ]

        async with client as c:
            for feedback in feedback_list:
                response = await c.post(
                    "/feedback", json=feedback, headers=authenticated_user
                )
                assert response.status_code == 201

            # Check that all feedback was created
            summary_response = await c.get(
                "/feedback/summary", headers=authenticated_user
            )
            summary_data = summary_response.json()
            assert summary_data["total_feedback"] >= len(feedback_list)
