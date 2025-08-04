# CHANGES.md

## 🔧 Task 1: User Management API (Refactor)

### 🛑 Problems Identified

1. **Monolithic Codebase**
   - All logic (routing, DB, validation) in a single file (`app.py`)
   - Difficult to maintain or scale

2. **Security Issues**
   - No use of environment variables for sensitive config (`SECRET_KEY`)
   - No CSRF/auth token support (expected in production-grade APIs)

3. **Validation Gaps**
   - Incomplete input validation on endpoints
   - Inconsistent error handling and HTTP status codes

4. **Database Management**
   - DB connections managed in a procedural way, risking leaks
   - No centralized `get_db()` function reuse

5. **Testing**
   - No tests included in the original legacy code

---

### ✅ Changes Made

| Area | Refactor Summary |
|------|------------------|
| 🔄 **Structure** | Introduced Flask Blueprint (`routes/users.py`), created `db.py`, and `__init__.py` with `create_app()` |
| 🔐 **Security** | Added password hashing (`generate_password_hash`), UNIQUE email checks, and used `SECRET_KEY` |
| ✅ **Validation** | Implemented strict checks on all inputs and returned appropriate HTTP status codes |
| 🧪 **Testing** | Added basic `pytest` tests for home, login failure, and missing field errors |
| 🗃️ **Database Init** | Moved DB schema logic to `init_db.py` for separation |
| 🚀 **Modularization** | Created clean `app/` folder for reusable components |

---

### 💭 Assumptions & Trade-offs

- Stayed with **Flask** and **SQLite** for simplicity and minimal setup
- Avoided switching to a framework like FastAPI to stay close to the original stack
- Used basic Python validation instead of a schema library (e.g., Pydantic or Marshmallow)

---

### 🧪 What I Would Do With More Time

- Add input schema validation with Marshmallow or Pydantic
- Use `.env` for config (with `python-dotenv`)
- Add JWT-based authentication
- Write integration and edge case tests
- Migrate to a production-ready DB like PostgreSQL
- Add Docker support for easy setup

---

## 🚀 Task 2: URL Shortener (New Feature)

### ✅ Built Features

1. `POST /api/shorten` — Generates a short code for valid URLs
2. `GET /<shortcode>` — Redirects to original URL
3. `GET /api/stats/<shortcode>` — Returns analytics (clicks, creation time)
4. URL validation using regex
5. Short code generation using secure random logic

---

### 🧪 Testing Added

- Home endpoint check
- Invalid URL shortening test
- Login failure (reused test client)

---

### 💡 Future Improvements

- Track user-level shortening/authentication
- Expiry for links
- Rate limiting to avoid abuse
- Real-time analytics with timestamp logging
- Frontend UI for shortening and tracking

---

## 🤖 AI Usage Disclosure

I used **ChatGPT** for:
- Suggesting Flask structure and best practices
- Code cleanup guidance (Blueprint, modular design)
- Drafting parts of `CHANGES.md` and test functions

All AI-generated code was reviewed and manually edited or replaced to ensure correctness and relevance.

---

