from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database

def get_engine(user, password, host, port, database):
    url = f'postgresql://{user}:{password}@{host}:{port}/{database}'
    if not database_exists(url):
        create_database(url)
        print(f"Database {database} created successfully.")
    engine = create_engine(url, echo=True)
    return engine

engine = get_engine('postgres', '1234', 'localhost', '5432', 'bostadsdata')