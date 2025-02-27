"""
This script performs initial data migrations for the Resume API project.
It uses SQLAlchemy's metadata to create or update the necessary database schema in PostgreSQL.
Before starting the application, run this script to generate fake data.

Execute this script by running:
    >>  python data_migration.py

Note: Data is fake!!!, For testing purposes only.
"""

# Imports
import random
from faker import Faker
from sqlalchemy import create_engine, text, inspect
from sqlalchemy.orm import sessionmaker

from constants import DATABASE_CREDENTIALS
from models import Resume
from database import Base


degrees = [
    'B.Tech', 'MBA', 'MBBS', 'Dentist', 'BBA', 'CA', 'BA', 'B.COM',
    'M.Tech', 'MS', 'MD', 'B.Arch', 'LLB', 'M.Sc', 'MA', 'B.Sc',
    'M.Phil', 'Ph.D', 'BFA', 'MCA'
]

institutions = [
    'IIT Bombay', 'Stanford University', 'Harvard Medical School',
    'AIIMS Delhi',
    'IIM Ahmedabad', 'Oxford University', 'Cambridge University', 'MIT',
    'University of Tokyo', 'National University of Singapore',
    'Peking University',
    'ETH Zurich', 'California Institute of Technology',
    'Imperial College London',
    'University of Toronto', 'University of Melbourne', 'Kyoto University',
    'Seoul National University', 'Technical University of Munich',
    'École Polytechnique Fédérale de Lausanne',
    'University of California, Berkeley', 'Princeton University',
    'Yale University',
    'Columbia University', 'Johns Hopkins University', 'University of Chicago',
    'University of Pennsylvania', 'Cornell University', 'Duke University',
    'University of Michigan'
]

skills = [
    "Python", "Programming", "Data Analysis", "Machine Learning",
    "Graphic Design", "Video Editing", "Digital Marketing",
    "Project Management",
    "Public Speaking", "Creative Writing", "Financial Analysis", "Sales",
    "Customer Service", "Foreign Language Proficiency (Spanish)",
    "Cloud Computing (AWS)",
    "Network Administration", "Cybersecurity", "Mobile App Development",
    "UI/UX Design",
    "Content Creation", "SEO Optimization", "Statistical Analysis",
    "Data Visualization",
    "Database Management (SQL)", "Game Development", "Photography",
    "Film Making",
    "Animation", "Technical Writing", "Blockchain Development",
    "Web Development",
    "AWS EC2", "Web Scraping", "AI/ML", "WEB3", "Sales", "HR", "Marketing",
    "Java", "Django", "Flask", "Postgres", "Pharma", "Interviewing",
    "Content Creator",
    "C/C++", "Foreign Language Proficiency (English)", "Gaming",
    "Video Editing",
    "Singing", "Dancing", "Motivational Speaker", "Golang", "React",
    "API Integration & Development", "Backend Development"
]


DATABASE_URL_SYNC = (
    f"postgresql://{DATABASE_CREDENTIALS['user']}:"
    f"{DATABASE_CREDENTIALS['password']}@{DATABASE_CREDENTIALS['host']}:"
    f"{DATABASE_CREDENTIALS['port']}/{DATABASE_CREDENTIALS['database']}"
)
engine_sync = create_engine(DATABASE_URL_SYNC)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine_sync)


def check_create_database(database_url: str):
    """
    Check if the database exists; if not, create it.
    """
    # Derive the default connection URL by replacing the database with 'postgres'
    default_url = database_url.rsplit('/', 1)[0] + '/postgres'
    engine_default = create_engine(default_url)

    with engine_default.connect() as conn:
        result = conn.execute(
            text("SELECT 1 FROM pg_database WHERE datname='resumedb'")
        )
        exists = result.scalar() is not None
        if not exists:
            conn.execute(text("COMMIT"))
            conn.execute(text("CREATE DATABASE resumedb"))
            print("Database 'resumedb' created!!")
        else:
            print("Database 'resumedb' already exists!")
    engine_default.dispose()


def create_dummy_data(n: int = 100):
    fake = Faker()
    session = SessionLocal()
    for _ in range(n):
        resume = Resume(
            full_name=fake.name(),
            email=fake.email(),
            phone=fake.phone_number(),
            linkedin_url=fake.url(),
            education=[{
                "degree": random.choice(degrees),
                "institution": random.choice(institutions),
                "year": fake.year()
            }],
            work_experience=[{
                "company": fake.company(),
                "role": fake.job(),
                "duration": f"{fake.random_int(min=1, max=5)} years"
            }],
            skills=[random.choice(skills) for _ in range(fake.random_int(min=1, max=5))]
        )
        session.add(resume)
    session.commit()
    session.close()
    print(f"Inserted {n} dummy resumes.")


if __name__ == '__main__':

    raise_exp = False
    try:
        num = int(
            input("\033[1;32mPlease enter the amount of dummy data needed: \033[0m")
        )
        if num < 0:
            raise_exp = True
    except ValueError:
        raise_exp = True

    if raise_exp:
        raise Exception(
            "\033[1;31m\033[1mPlease enter a valid number greater than ZERO!\033[0m"
        )

    print('\n', "*" * 40)
    # Check and create the 'resumedb' database if it does not exist.
    check_create_database(DATABASE_URL_SYNC)

    # Check and create the 'resumes' table if it does not exist.
    inspector = inspect(engine_sync)
    if "resumes" not in inspector.get_table_names():
        print("Table 'resumes' does not exist. Creating it...")
        print('\n', "*" * 40)
        print(f"Creating {num} data!")
        Base.metadata.create_all(bind=engine_sync)
    else:
        print("Table 'resumes' already exists!")
        print('\n', "*" * 40)
        print(f"Recreating {num} data!")
        Base.metadata.drop_all(bind=engine_sync)
        Base.metadata.create_all(bind=engine_sync)

    # Insert dummy data.
    create_dummy_data(num)
    print('*** Your database is ready to go!!! ***')
