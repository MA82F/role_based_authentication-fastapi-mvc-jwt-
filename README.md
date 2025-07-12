# FastAPI Role-Based Feedback Collector API

A containerized FastAPI application with JWT authentication, user/role management, and feedback submission APIs built with MVC-modular architecture.

## 🏗️ Project Structure

```
app/
├── __init__.py
├── main.py                 # FastAPI app entry point
├── core/                   # Core functionality
│   ├── __init__.py
│   ├── config.py          # Settings and configuration
│   ├── database.py        # Database connection
│   └── security.py        # JWT and password utilities
├── auth/                   # Authentication module
│   ├── __init__.py
│   ├── controller.py      # Auth endpoints
│   ├── service.py         # Auth business logic
│   ├── schemas.py         # Auth Pydantic models
│   └── dependencies.py    # JWT dependencies
├── user/                   # User module
│   ├── __init__.py
│   ├── model.py           # User SQLAlchemy model
│   ├── controller.py      # User endpoints
│   ├── service.py         # User business logic
│   └── schemas.py         # User Pydantic models
├── role/                   # Role module
│   ├── __init__.py
│   ├── controller.py      # Role endpoints
│   ├── service.py         # Role business logic
│   └── schemas.py         # Role Pydantic models
└── feedback/               # Feedback module
    ├── __init__.py
    ├── model.py           # Feedback SQLAlchemy model
    ├── controller.py      # Feedback endpoints
    ├── service.py         # Feedback business logic
    └── schemas.py         # Feedback Pydantic models
```

## 🚀 Quick Start

### Using Docker (Recommended)

1. **Clone and navigate to project:**

   ```bash
   cd fastapi
   ```

2. **Start the application:**

   ```bash
   docker-compose up --build
   ```

3. **Access the API:**
   - API: http://localhost:8000
   - Documentation: http://localhost:8000/docs
   - Alternative docs: http://localhost:8000/redoc

### Local Development

1. **Create virtual environment:**

   ```bash
   python -m venv env
   env\Scripts\activate  # Windows
   ```

2. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Set up PostgreSQL and update .env file**

4. **Run the application:**
   ```bash
   uvicorn app.main:app --reload
   ```

## 📋 API Endpoints

### 🔐 Authentication

- `POST /auth/signup` - Register new user
- `POST /auth/login` - Login and get JWT token

### 👤 User Management

- `GET /user/profile` - Get current user profile (Auth required)
- `GET /admin/users` - List all users (Admin only)
- `PATCH /admin/users/{id}` - Update user (Admin only)

### 🛡️ Role Management

- `PATCH /admin/roles/{user_id}` - Change user role (Admin only)

### 💬 Feedback

- `POST /user/feedback` - Submit feedback (Auth required)
- `GET /admin/feedback` - View all feedback (Admin only)
- `GET /feedback/summary` - Get feedback summary (Public)

## 🧪 Testing

```bash
pytest test_main.py -v
```

## 🔑 Key Features

- **MVC Architecture**: Clean separation of concerns
- **JWT Authentication**: Secure token-based auth
- **Role-Based Access**: User and Admin roles
- **SQLAlchemy ORM**: Database abstraction
- **Pydantic Validation**: Request/response validation
- **Docker Support**: Easy deployment
- **Automatic Documentation**: Swagger UI included

## 📝 Example Usage

### 1. Register a user:

```bash
curl -X POST "http://localhost:8000/auth/signup" \
     -H "Content-Type: application/json" \
     -d '{
       "username": "john_doe",
       "email": "john@example.com",
       "password": "securepassword"
     }'
```

### 2. Login:

```bash
curl -X POST "http://localhost:8000/auth/login" \
     -H "Content-Type: application/json" \
     -d '{
       "username": "john_doe",
       "password": "securepassword"
     }'
```

### 3. Submit feedback (with JWT token):

```bash
curl -X POST "http://localhost:8000/user/feedback" \
     -H "Authorization: Bearer YOUR_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{
       "rating": 5,
       "comment": "Great service!"
     }'
```

## 🛠️ Development Tips

1. **Understanding MVC Structure:**

   - **Models**: Define data structure (SQLAlchemy)
   - **Controllers**: Handle HTTP requests/responses (FastAPI routes)
   - **Services**: Contains business logic (reusable functions)

2. **Authentication Flow:**

   - User signs up → password is hashed
   - User logs in → JWT token is created
   - Protected routes require valid JWT token
   - Admin routes check user role

3. **Adding New Features:**
   - Create model in `{module}/model.py`
   - Define schemas in `{module}/schemas.py`
   - Implement business logic in `{module}/service.py`
   - Create API endpoints in `{module}/controller.py`
   - Register router in `main.py`

## 🔧 Configuration

Environment variables in `.env`:

- `DATABASE_URL`: PostgreSQL connection string
- `SECRET_KEY`: JWT secret key
- `DEBUG`: Enable debug mode

## 📚 Tech Stack

- **FastAPI**: Modern Python web framework
- **SQLAlchemy**: SQL toolkit and ORM
- **PostgreSQL**: Database
- **JWT**: Authentication
- **Docker**: Containerization
- **Pytest**: Testing framework
