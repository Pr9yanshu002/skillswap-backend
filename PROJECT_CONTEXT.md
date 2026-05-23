# SkillSwap Backend - Project Context

## Project Identity

- **Name:** `SkillSwap Backend`
- **Type:** REST API backend for a peer-to-peer mentorship and learning platform
- **Framework:** Django + Django REST Framework
- **Authentication:** JWT via SimpleJWT

## Tech Stack and Tools

### Runtime and Core Framework

- Python 3.12 (CI runtime)
- Django 6.0.1
- Django REST Framework 3.16.1

### Authentication and Security

- djangorestframework_simplejwt 5.5.1
- PyJWT 2.10.1

### Database and Storage

- dj-database-url 3.1.2 (DATABASE_URL parsing)
- psycopg2-binary 2.9.11 (PostgreSQL adapter)
- SQLite fallback for local development
- Pillow 12.1.0 (image field support)

### HTTP, Static, and CORS

- gunicorn 25.1.0 (WSGI server)
- whitenoise 6.12.0 (static file serving in production)
- django-cors-headers 4.9.0

### Dev/Utility

- python-dotenv 1.2.1
- asgiref, packaging, sqlparse

### CI/CD

- GitHub Actions workflow: `.github/workflows/backend.yml`
- CI checks:
  - `python manage.py makemigrations --check`
  - `python manage.py check`

## Repository Structure

- `core/` - Django project settings, root URL config, WSGI/ASGI
- `users/` - Auth, user profiles, skills, mentor discovery
- `booking/` - Session booking and slot workflows
- `utils/google_meet.py` - Jitsi link generation utility
- `.github/workflows/backend.yml` - CI pipeline
- `Procfile` - process command for deployment
- `requirements.txt` - Python dependencies

## Configuration and Environment

### Important settings

- `SECRET_KEY` from environment with local fallback
- `DEBUG = True` (currently hardcoded)
- `ALLOWED_HOSTS = ["127.0.0.1", "localhost", ".onrender.com"]`
- `AUTH_USER_MODEL = "users.User"`
- DRF default auth: JWT
- DRF default permissions: authenticated by default
- Static files via WhiteNoise:
  - `STATIC_ROOT = BASE_DIR / "staticfiles"`
  - `CompressedManifestStaticFilesStorage`

### Expected environment variables

- `SECRET_KEY`
- `DATABASE_URL`

## Data Model

### Users domain

- **User** (extends `AbstractUser`)
  - `email` (unique, used as username field)
  - `bio`
  - `profile_image`
- **Skill**
  - `name` (unique)
  - `category` (programming/music/sports/art/language/other)
  - `is_active`
- **UserSkill**
  - Link between user and skill
  - `level` (beginner/intermediate/advanced)
  - `can_teach`, `can_learn`
  - unique constraint on `(user, skill)`

### Booking domain

- **Session**
  - `mentor`, `learner`
  - `userSkill`
  - `message`
  - `meet_link`
  - `status` (pending/accepted/rejected/scheduled/completed)
  - `selected_slot`
- **SessionSlot**
  - Belongs to a session
  - Proposed by user
  - `start_time`, `end_time`
  - `is_selected`

## API Endpoints

### Auth and user

- `POST /api/auth/register/` - Register account
- `GET /api/auth/me/` - Current authenticated user profile
- `POST /api/auth/login/` - Obtain JWT pair
- `POST /api/auth/token/refresh/` - Refresh token

### Skills and mentor discovery

- `GET /api/skills/` - List/search active skills (`?search=`), capped to 10
- `POST /api/users/skills/` - Add skill mapping for current user
- `GET /api/users/me/skills/` - List current user skill mappings
- `GET /api/mentors/?skill=<id>` - List mentors, optional skill filter
- `GET /api/mentors/<pk>/` - Mentor profile (`UserSkill` pk)
- `GET /api/users/<pk>/` - User profile by user id

### Sessions and booking

- `GET/POST /api/sessions/` - List or create sessions (`?role=mentor|learner`)
- `PATCH /api/sessions/<pk>/` - Mentor updates session status
- `POST /api/sessions/<pk>/slots/` - Mentor proposes session slots (max 5)
- `PATCH /api/slots/<pk>/select/` - Learner selects slot and schedules session

## Business Rules

- Duplicate pending requests for same learner and `userSkill` are blocked.
- Only mentor can update session status.
- Session status transitions are validated.
- Only mentor can propose slots, only after session is accepted.
- Maximum 5 slots per session.
- Only learner can select a slot.
- Slot selection is atomic and ensures consistency.
- On slot selection:
  - Session becomes `scheduled`
  - Meet link generated via Jitsi URL helper
  - Non-selected slots are removed
- For `UserSkill`, at least one of `can_teach` or `can_learn` is required.

## Deployment Context

### Configured in repo

- `Procfile`: `web: gunicorn core.wsgi:application`
- WhiteNoise static serving
- Host allow-list includes `.onrender.com`
- Env-driven secret/database configuration

### Likely deployment target

- Render (inferred from host pattern and Procfile usage)

### Not present in repo

- No `Dockerfile` or `docker-compose.yml`
- No explicit `render.yaml`, Terraform, or Kubernetes manifests
- No automated deployment step in CI workflow

## CI and Testing Status

- CI runs on pushes to `main`.
- Current checks are migration consistency and Django health check.
- `users/tests.py` and `booking/tests.py` exist but are placeholders.
- No implemented API/unit test suite yet.

## Local Development Workflow

1. Install dependencies:
   - `pip install -r requirements.txt`
2. Apply migrations:
   - `python manage.py migrate`
3. Seed skills:
   - `python manage.py seed_skills`
4. Run server:
   - `python manage.py runserver`

## Security and Production Notes

- `DEBUG` should be env-driven and disabled in production.
- `CORS_ALLOW_ALL_ORIGINS = True` is too permissive for production.
- Secret key fallback is for local use only.
- Rate limiting and detailed observability are not configured yet.

## Short Pasteable Context

SkillSwap Backend is a Django 6 and DRF API with JWT authentication, custom email-based users, skill catalog and user-skill mapping, mentor discovery, and a full booking lifecycle. Learners request mentor sessions, mentors accept/reject, mentors propose time slots, and learners select one slot; selection atomically schedules the session and creates a Jitsi meet link. Data model centers on User, Skill, UserSkill, Session, and SessionSlot. The app is configured for env-based DB/secret values with local SQLite fallback and PostgreSQL intent, served with Gunicorn and WhiteNoise, and likely deployed on Render. CI uses GitHub Actions for migration and system checks, while tests are currently placeholders.
