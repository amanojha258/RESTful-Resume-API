import os
# from dotenv import load_dotenv
# load_dotenv()

# Add database credentials here.
DATABASE_CREDENTIALS = {
    "user": os.getenv("DATABASE_USER", "****"),
    "password": os.getenv("DATABASE_PASSWORD", "****"),
    "host": os.getenv("DATABASE_HOST", "localhost"),
    "port": os.getenv("DATABASE_PORT", "5432"),
    "database": os.getenv("DATABASE_NAME", "resumedb"),
}


SECRET_KEY = os.getenv("SECRET_KEY", "MySecretKey")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = 30


# Dummy user data for demonstration purposes.
FAKE_USER_DATA = {
    "admin": {
        "username": "admin",
        "password": "secret"
    }
}
