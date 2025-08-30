# Bill Station Authentication System

A secure Django-based authentication system for Bill Station fintech company with JWT tokens, Redis caching, and password reset functionality.

## Quick Start

### Docker (Recommended)
```bash
git clone <repository-url>
cd auth_system
docker-compose up -d
```
- **API**: http://localhost:8000/api/
- **Swagger**: http://localhost:8000/api/docs/

## Features

- **Email-based authentication** (no username required)
- **JWT token authentication** with refresh tokens
- **Password reset** with Redis-cached tokens
- **Rate limiting** on sensitive endpoints
- **CORS support** for frontend integration
- **Swagger/OpenAPI documentation**
- **Comprehensive test coverage**

## Prerequisites

- Python
- Redis (for caching and password reset tokens)
- PostgreSQL (for production) or SQLite (for development)

## Setup Instructions

### 1. Clone the repository
```bash
git clone <repository-url>
cd <root_folder_name>
```

### 2. Create virtual environment
```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run database migrations
```bash
python backend/manage.py migrate
```

### 5. Create a superuser (optional) for admin access
```bash
python backend/manage.py createsuperuser
```

### 6. Start the development server
```bash
# Activate virtual environment
source .venv/bin/activate

# Run the development server
python backend/manage.py runserver

# The server will start at http://localhost:8000
```

### 7. Running Tests
```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest test/test_auth.py
```

## Environment Variable Details

### Required Environment Variables

Create a `.env` file in the root directory

### Example .env file
```bash
# Django settings
SECRET_KEY=your-secret-key-here
DEBUG=1
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
# Redis (for caching and password reset)
REDIS_URL=redis://localhost:6379/1

```

### Rate Limiting Configuration

| Endpoint | Development Rate | Production Rate |
|----------|------------------|-----------------|
| Login | 100/minute | 5/minute |
| Password Reset | 100/minute | 5/minute |
| Anonymous Users | 1000/day | 100/day |
| Authenticated Users | 10000/day | 1000/day |

## API Endpoint Documentation

### Base URL: `http://localhost:8000/api/`

### Interactive Documentation
- **Swagger UI**: http://localhost:8000/api/docs/
- **OpenAPI Schema**: http://localhost:8000/api/schema/

### Authentication Endpoints

| Endpoint | Method | Description | Authentication | Rate Limit |
|----------|--------|-------------|----------------|------------|
| `/register` | POST | Register new user | None | None |
| `/login` | POST | Login and get JWT tokens | None | 5/minute |
| `/token/refresh` | POST | Refresh access token | None | None |
| `/profile` | GET | Get user profile | JWT Required | None |
| `/forgot-password` | POST | Request password reset | None | 5/minute |
| `/reset-password` | POST | Reset password with token | None | 5/minute |

### Request/Response Examples

#### 1. User Registration
```bash
curl -X POST http://localhost:8000/api/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securepassword123",
    "full_name": "John Doe"
  }'
```

**Response:**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "email": "user@example.com",
    "full_name": "John Doe"
  }
}
```

#### 2. User Login
```bash
curl -X POST http://localhost:8000/api/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securepassword123"
  }'
```

**Response:**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

#### 3. Access Protected Endpoint
```bash
curl -H "Authorization: Bearer <access_token>" \
  http://localhost:8000/api/profile
```

**Response:**
```json
{
  "id": 1,
  "email": "user@example.com",
  "full_name": "John Doe"
}
```

#### 4. Password Reset Flow
```bash
# Step 1: Request password reset
curl -X POST http://localhost:8000/api/forgot-password \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com"}'

# Response includes reset token
{
  "success": true,
  "token": "reset_token_here"
}

# Step 2: Reset password
curl -X POST http://localhost:8000/api/reset-password \
  -H "Content-Type: application/json" \
  -d '{
    "token": "reset_token_here",
    "password": "newpassword123"
  }'

# Response
{
  "success": true
}
```

### JWT Token Details

- **Access Token Lifetime**: 15 minutes
- **Refresh Token Lifetime**: 7 days
- **Token Type**: Bearer
- **Algorithm**: HS256

### Error Responses

| Status Code | Description | Example |
|-------------|-------------|---------|
| 400 | Bad Request | Invalid email format |
| 401 | Unauthorized | Invalid credentials |
| 429 | Too Many Requests | Rate limit exceeded |
| 500 | Internal Server Error | Server error |

## Deployment Link

### Docker Deployment

1. **Build the Docker image:**
```bash
docker build -t billstation-auth .
```

2. **Run with Docker Compose:**
```bash
docker-compose up -d
```

3. **Access the deployed application:**
- **Production URL**: https://your-domain.com/api/
- **Swagger Docs**: https://your-domain.com/api/docs/

### Manual Deployment

1. **Set production environment variables:**
```bash
export DEBUG=0
export SECRET_KEY=your-production-secret-key
export DATABASE_URL=postgresql://user:pass@host:5432/db
export REDIS_URL=redis://host:6379/1
```

2. **Collect static files:**
```bash
python backend/manage.py collectstatic
```

3. **Run with Gunicorn:**
```bash
gunicorn backend.core.wsgi:application --bind 0.0.0.0:8000
```

### Platform Deployment

#### Render
- **Deployment URL**: https://your-app.onrender.com/api/
- **Documentation**: https://your-app.onrender.com/api/docs/


### Environment Setup for Deployment

```bash
# Production environment variables
SECRET_KEY=your-super-secure-production-key
DEBUG=0
DATABASE_URL=postgresql://user:password@host:5432/dbname
REDIS_URL=redis://host:6379/1
ALLOWED_HOSTS=your-domain.com,www.your-domain.com
```

## Project Structure

```
auth_system/
├── backend/
│   ├── core/                 # Django project settings
│   │   ├── settings.py      # Main settings
│   │   ├── urls.py          # Main URL configuration
│   │   └── wsgi.py          # WSGI application
│   ├── users/               # Authentication app
│   │   ├── models.py        # Custom User model
│   │   ├── views.py         # API views
│   │   ├── serializers.py   # Data serialization
│   │   └── urls.py          # API endpoints
│   └── manage.py            # Django management
├── test/
│   └── test_auth.py         # Test suite
├── requirements.txt          # Python dependencies
├── pytest.ini              # Test configuration
└── README.md               # This file
```

## Security Features

- **JWT tokens** with configurable expiration
- **Password hashing** using Django's secure methods
- **Rate limiting** to prevent brute force attacks
- **CORS configuration** for secure cross-origin requests
- **Redis caching** for password reset tokens


