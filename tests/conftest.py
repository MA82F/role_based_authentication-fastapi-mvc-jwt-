import pytest
import asyncio
from httpx import AsyncClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.core.database import get_db, Base

# Create test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


@pytest.fixture(scope="function", autouse=True)
def setup_test_db():
    """Create test database tables for each test"""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    app.dependency_overrides[get_db] = override_get_db
    yield
    app.dependency_overrides.clear()


@pytest.fixture
def client():
    """FastAPI async test client"""
    return AsyncClient(app=app, base_url="http://test")


@pytest.fixture
def test_user_data():
    """Sample user data for testing"""
    return {
        "username": "testuser",
        "email": "test@example.com", 
        "password": "testpassword123"
    }


@pytest.fixture
def test_admin_data():
    """Sample admin data for testing"""
    return {
        "username": "admin",
        "email": "admin@example.com",
        "password": "adminpassword123"
    }


@pytest.fixture
def authenticated_user():
    """Return a function to create authenticated user headers"""
    async def _create_authenticated_user(client, test_user_data):
        # Create user (don't use async with here since client is already open)
        await client.post("/auth/signup", json=test_user_data)
        
        # Login and get token
        login_response = await client.post(
            "/auth/login", 
            json={"username": test_user_data["username"], "password": test_user_data["password"]}
        )
        token = login_response.json()["access_token"]
        return {"Authorization": f"Bearer {token}"}
    
    return _create_authenticated_user


@pytest.fixture
def authenticated_admin():
    """Return a function to create authenticated admin headers"""
    async def _create_authenticated_admin(client, test_admin_data):
        from app.user.model import User
        from app.core.security import get_password_hash
        
        # Create admin user directly in database
        db = TestingSessionLocal()
        try:
            hashed_password = get_password_hash(test_admin_data["password"])
            admin_user = User(
                username=test_admin_data["username"],
                email=test_admin_data["email"],
                hashed_password=hashed_password,
                role="admin"
            )
            db.add(admin_user)
            db.commit()
        finally:
            db.close()
        
        async with client as c:
            # Login and get token
            login_response = await c.post(
                "/auth/login", 
                json={"username": test_admin_data["username"], "password": test_admin_data["password"]}
            )
            token = login_response.json()["access_token"]
            return {"Authorization": f"Bearer {token}"}
    
    return _create_authenticated_admin
