# keylin

[![Python Versions](https://img.shields.io/pypi/pyversions/keylin)](https://pypi.org/project/keylin)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Tests](https://github.com/beanone/keylin/actions/workflows/tests.yml/badge.svg)](https://github.com/beanone/keylin/actions?query=workflow%3Atests)
[![Coverage](https://codecov.io/gh/beanone/keylin/branch/main/graph/badge.svg)](https://codecov.io/gh/beanone/keylin)
[![Code Quality](https://img.shields.io/badge/code%20style-ruff-000000)](https://github.com/astral-sh/ruff)
[![PyPI version](https://img.shields.io/pypi/v/keylin)](https://pypi.org/project/keylin)

## Features

- User model and schema library for authentication services
- Designed for integration with FastAPI and fastapi-users
- Reusable across multiple services
- Internal async API key management (CRUD) module

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [API Key Management](#api-key-management)
- [Architecture & Integration Guide](#architecture--integration-guide)
- [User Model & Database Schema](#user-model--database-schema)
- [Configuration Usage](#configuration-usage)
- [Testing](#testing)
- [Setting Up the User Database](#setting-up-the-user-database)
- [Admin User Account Setup](#admin-user-account-setup)
- [License](#license)

## Installation

```bash
pip install keylin
```

## Usage

```python
from keylin.models import User
from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from keylin.db import get_async_session

app = FastAPI()

@app.get("/users/{user_id}")
async def get_user(user_id: str, session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(
        User.__table__.select().where(User.id == user_id)
    )
    user = result.fetchone()
    if user:
        return user
    return {"error": "User not found"}
```

## API Key Management

Keylin includes an internal API key management module (`keylin.apikey_manager`) that provides async functions for creating, listing, and deleting API keys. These functions encapsulate all business logic and database operations for API key management and are intended for use within the keylin codebase.

- `create_api_key(user_id, service_id, session, name=None, expires_at=None)`
- `list_api_keys(user_id, session)`
- `delete_api_key(key_id, user_id, session)`

All functions are async and require an `AsyncSession` for database access.

## Architecture & Integration Guide

### Typical Architecture

A recommended architecture for a login/authentication service using `keylin`:

```mermaid
graph TD
    A[Client App / Frontend]
    B[API Gateway / HTTPS Proxy]
    C[FastAPI Login Service - uses keylin]
    D[Database - PostgreSQL, etc.]
    A --> B
    B --> C
    C --> D
```

- **keylin** provides the user model, schemas, and authentication logic.
- The login service is a FastAPI app that imports keylin and wires up routers.
- Other services can import keylin to share the user model and schemas for consistent user data handling.

### Example FastAPI Login Service

```python
from fastapi import FastAPI
from keylin.auth import auth_backend, fastapi_users, get_user_manager
from keylin.schemas import UserRead, UserCreate

app = FastAPI()

# Auth routes
app.include_router(fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["auth"])
app.include_router(fastapi_users.get_register_router(UserRead, UserCreate), prefix="/auth", tags=["auth"])
app.include_router(fastapi_users.get_users_router(UserRead, UserRead), prefix="/users", tags=["users"])
```

### Environment Variables (Required for Production)
- `JWT_SECRET`: Secret key for JWT signing (**required**; application will raise an error if not set)
- `RESET_PASSWORD_SECRET`: Secret for password reset tokens (optional, defaults to JWT secret)
- `VERIFICATION_SECRET`: Secret for verification tokens (optional, defaults to JWT secret)
- `DATABASE_URL`: SQLAlchemy DB URL (e.g., `postgresql+asyncpg://user:pass@host/dbname`)

> **Note:** If `JWT_SECRET` is not set, the application will raise a `RuntimeError` at startup.

### Security & Deployment Best Practices
- **CORS:** Configure CORS in your FastAPI app using `CORSMiddleware` to restrict allowed origins.
- **HTTPS:** Always deploy behind a TLS-terminating proxy (e.g., NGINX, Caddy, cloud load balancer).
- **Secret Management:** Never hardcode secrets. Use environment variables or a secrets manager.
- **Rate Limiting:** Add rate limiting at the API gateway or with middleware to prevent brute-force attacks.
- **Email Verification:** Enable and configure email verification in your login service for new users.
- **Audit Logging:** Log authentication events for security monitoring.

### Extending the User Model
- You can add fields to the `User` model and corresponding Pydantic schemas in your own code or by forking/extending keylin.
- All models and schemas use type annotations and are compatible with FastAPI and Pydantic.

### User Model & Database Schema

#### Default User Model Fields

| Field            | Type      | Description                 | Required | Notes                |
|------------------|-----------|-----------------------------|----------|----------------------|
| id               | UUID      | Unique user identifier      | Yes      | Primary key          |
| email            | str       | User email (unique)         | Yes      | Unique, indexed      |
| hashed_password  | str       | Hashed password             | Yes      | Not exposed in API responses |
| full_name        | str/None  | User's full name            | No       | Optional             |
| is_active        | bool      | Is the user active?         | Yes      |                      |
| is_superuser     | bool      | Is the user an admin?       | Yes      |                      |
| is_verified      | bool      | Has the user verified email | Yes      |                      |

> **Note:** The table is named `"user"`, which is a reserved word in some databases (e.g., PostgreSQL). Consider renaming to `"users"` if you encounter issues.

#### Example User Schema

```json
{
  "id": "uuid",
  "email": "user@example.com",
  "full_name": "User Name",
  "is_active": true,
  "is_superuser": false,
  "is_verified": true
}
```

#### Extending the User Model
- To add fields, update the `User` SQLAlchemy model and the corresponding Pydantic schemas.
- Run a new Alembic migration to update the database schema.
- Update the UI to handle new fields as needed.
- Keep the UI and backend in sync regarding user data shape.
- **Tip:** If you need roles or permissions, add fields (e.g., `role`, `permissions`) to the model and schemas, and update your business logic accordingly.

### Configuration Usage

The `keylin.config.Settings` class provides all configuration via environment variables or a `.env` file. **There is no longer a global `settings` singleton.**

- To use configuration, import and instantiate `Settings` directly:

```python
from keylin.config import Settings
settings = Settings()
```

- If you are building a service that needs additional configuration, subclass `Settings`:

```python
from keylin.config import Settings as KeylinSettings

class MyServiceSettings(KeylinSettings):
    MY_SERVICE_API_KEY: str

settings = MyServiceSettings()
```

- All environment variables must be set before instantiating `Settings`.
- `JWT_SECRET` **must** be set, or a `RuntimeError` will be raised at startup.

### Testing
- The test suite sets `JWT_SECRET` automatically for all tests (see `tests/conftest.py`).
- All code and tests should instantiate `Settings` directly as needed.
- There is no global singleton; each test or module should create its own `Settings` instance if configuration is needed.
- See `tests/unit/test_keylin.py` and `tests/unit/test_apikey_manager.py` for example tests and mocking patterns.

### Setting Up the User Database

Before running your login service, you need to ensure the user table exists in your database.

#### Recommended: Use Alembic for Migrations
For production and team environments, use [Alembic](https://alembic.sqlalchemy.org/) to manage database migrations:

```bash
alembic revision --autogenerate -m "create user table"
alembic upgrade head
```

Make sure your Alembic `env.py` includes the keylin model's metadata:
```python
from keylin.models import Base

target_metadata = Base.metadata
```

#### Quick Local Setup: Create Tables Programmatically
For local development or quick tests, you can create the tables directly using SQLAlchemy:

```python
from keylin.models import Base
from sqlalchemy import create_engine

engine = create_engine("sqlite:///./test.db")  # Or your DB URL
Base.metadata.create_all(engine)
```

> **Note:** For production, always use migrations to avoid data loss and ensure schema consistency.

### Admin User Account Setup

After the user tables are created (either via Alembic or programmatically), `keylin` will automatically create an admin (superuser) account if one does not already exist. This ensures you always have an initial admin user for your application.

**Default admin credentials:**
- Email: `admin@example.com`
- Password: `changeme`
- Full name: `Admin`

**Override defaults in production:**
Set the following environment variables before starting your app to change the admin account credentials:
- `ADMIN_EMAIL` (default: `admin@example.com`)
- `ADMIN_PASSWORD` (default: `changeme`)
- `ADMIN_FULL_NAME` (default: `Admin`)

> **Security Note:** Always override the default admin password and email in production environments!

The admin user is created only if no superuser exists in the database. If you delete the admin user, it will be recreated on the next app startup unless another superuser exists.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
