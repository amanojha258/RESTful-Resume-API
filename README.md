# Resume API

This is a RESTful API for managing resumes built with below-mentioned tech stack.
It supports authentication and provides endpoints to create, read, update, and delete resume records, 
along with search/filter capabilities by skill.

## Tech Stack
- **Language:** Python 3.8+
- **Framework:** FastAPI
- **Database:** Postgres
- **ORM:** SQLAlchemy
- **Authentication:** JWT tokens
- **Validation:** Pydantic


## Setup Instructions
Make sure to create a python virtual environment for the installations
1. **Install Dependencies:**  
   ```bash
   pip install fastapi "fastapi[standard]" python-multipart Faker sqlalchemy psycopg2 asyncpg pydantic python-jose[cryptography]

2. **Create database:**  This will create the required database and table along with dummy data.
   ```bash
   python data_migration.py

3. **Run FastAPI Server:**  
   ```bash
   fastapi dev main.py


## Features
- **Authentication:** Secure endpoints using JWT tokens.
- **CRUD Endpoints:** Create, read, update, and delete resume records.
- **Search/Filter:** Filter resumes by a specific skill.


## API Endpoints

### Authentication
- **POST /token**  
  - **Description:** Authenticates a user and returns a JWT token.
  - **Request:** Form data with `username` and `password` (e.g., username: `admin`, password: `secret`).
  - **Response:**  
    ```json
    {
      "access_token": "your_jwt_token",
      "token_type": "bearer"
    }
    ```

### Resume Endpoints
- **GET /resumes**  
  - **Description:** Returns a paginated list of resumes.
  - **Query Parameters:**
    - `skip`: Number of records to skip (default 0)
    - `limit`: Maximum number of records to return (default 100)
    - `skill`: (Optional) Filter resumes by a specific skill.
  - **Response:** List of resume objects.

- **GET /resumes/{resume_id}**  
  - **Description:** Returns full details of the resume with the given ID.

- **POST /resumes**  
  - **Description:** Creates a new resume.
  - **Request Body:** JSON containing resume details (full_name, email, phone, linkedin_url, education, work_experience, skills).
  - **Response:** The created resume object.

- **PUT /resumes/{resume_id}**  
  - **Description:** Updates an existing resume.
  - **Request Body:** JSON with the fields to update.
  - **Response:** The updated resume object.

- **DELETE /resumes/{resume_id}**  
  - **Description:** Deletes the resume with the given ID.
  - **Response:** 204 No Content if successful.

