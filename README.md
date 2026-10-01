# Blog & Content Management API

A backend-focused Blog and Content Management API built with **FastAPI**, **SQLAlchemy**, and **PostgreSQL**. The project includes JWT authentication, role-based authorization, CRUD operations, comments, categories, tags, search, pagination, database migrations, Docker containerization, and automated testing.

## Features

* User registration and login
* JWT-based authentication
* Role-based authorization with admin controls
* User activation and deactivation
* Blog post CRUD operations
* Post ownership and authorization
* Categories and tags
* Many-to-many relationship between posts and tags
* Comments on published posts
* Search posts by title or content
* Pagination for posts
* PostgreSQL database
* SQLAlchemy ORM
* Alembic database migrations
* Docker and Docker Compose
* Automated tests using Pytest
* Interactive API documentation with Swagger UI

## Tech Stack

* **Python**
* **FastAPI**
* **SQLAlchemy**
* **PostgreSQL**
* **JWT**
* **Alembic**
* **Docker**
* **Docker Compose**
* **Pytest**
* **Jinja2**

## Project Structure

```text
Project3/
├── app/
│   ├── routers/
│   │   ├── auth.py
│   │   ├── posts.py
│   │   ├── categories.py
│   │   ├── tags.py
│   │   ├── comments.py
│   │   └── users.py
│   ├── templates/
│   ├── static/
│   ├── auth_utils.py
│   ├── database.py
│   ├── dependencies.py
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   ├── DockerFile
│   ├── docker-compose.yml
│   └── requirements.txt
├── alembic/
│   ├── versions/
│   └── env.py
├── tests/
│   ├── conftest.py
│   ├── test_auth.py
│   ├── test_posts.py
│   ├── test_categories.py
│   ├── test_tags.py
│   ├── test_comments.py
│   └── test_users.py
├── alembic.ini
├── .env.example
├── .gitignore
└── README.md
```

## Authentication & Authorization

The API uses **JWT bearer tokens** for authentication.

Users can:

* Register an account
* Log in and receive an access token
* Access protected endpoints
* Create and manage their own posts
* Create and delete their own comments

Administrators can additionally:

* View all users
* Activate or deactivate users
* Delete posts created by other users
* Delete comments created by other users

Passwords are securely hashed before being stored in the database.

## Database Design

The application uses PostgreSQL with SQLAlchemy ORM.

Main entities:

```text
User
 │
 ├── Posts
 └── Comments

Post
 ├── User (Author)
 ├── Category
 ├── Tags
 └── Comments

Category
 └── Posts

Tag
 └── Posts
```

Posts and tags use a **many-to-many relationship** through the `post_tags` association table.

## API Documentation

After starting the application, Swagger UI is available at:

```text
http://localhost:8000/docs
```

The OpenAPI schema is available at:

```text
http://localhost:8000/openapi.json
```

## Running Locally

### 1. Clone the repository

```bash
git clone https://github.com/pratyus-dash/blog-api-fastapi.git
cd blog-api-fastapi
```

### 2. Create a virtual environment

Windows:

```powershell
python -m venv venv
```

Activate it:

```powershell
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
pip install -r app/requirements.txt
```

### 4. Configure environment variables

Create a `.env` file based on `.env.example`.

Example:

```env
DATABASE_URL=sqlite:///./blog.db
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 5. Run database migrations

```powershell
alembic upgrade head
```

### 6. Start the application

```powershell
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

## Running with Docker

The project includes Docker Compose configuration for running the FastAPI application with PostgreSQL.

From the project root:

```powershell
docker compose -f app/docker-compose.yml up --build
```

The application automatically runs the Alembic migrations when the container starts.

The API will be available at:

```text
http://localhost:8000
```

Swagger:

```text
http://localhost:8000/docs
```

To stop the containers:

```powershell
docker compose -f app/docker-compose.yml down
```

To stop the containers and remove the PostgreSQL volume:

```powershell
docker compose -f app/docker-compose.yml down -v
```

## Testing

The project contains automated tests using **Pytest**.

Run all tests from the project root:

```powershell
pytest
```

Current test coverage includes:

* User registration
* Duplicate users
* Login
* Invalid authentication
* JWT-protected routes
* Post creation and retrieval
* Post updates and deletion
* Authorization and ownership checks
* Search
* Pagination
* Categories
* Tags
* Comments
* Admin operations
* User activation/deactivation

The current test suite contains **45 automated tests**.

```text
45 passed
```

## Database Migrations

Alembic is used to manage database schema changes.

Create a new migration after modifying the SQLAlchemy models:

```powershell
alembic revision --autogenerate -m "describe change"
```

Apply migrations:

```powershell
alembic upgrade head
```

Rollback the latest migration:

```powershell
alembic downgrade -1
```

## Security

Sensitive configuration such as:

* Database credentials
* Secret keys
* Local database files
* Virtual environments

is excluded from Git using `.gitignore`.

Environment variables should be configured through `.env` locally and should not be committed to the repository.

## Future Improvements

Possible future improvements include:

* GitHub Actions CI/CD
* Cloud deployment
* Refresh tokens
* Rate limiting
* Improved frontend UI
* Production monitoring and logging
