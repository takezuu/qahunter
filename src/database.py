from sqlmodel import Session, create_engine

DATABASE_URL = "postgresql://postgres:newlife@78.153.150.29:5432/qahunter"
engine = create_engine(DATABASE_URL)

def get_session():
    with Session(engine) as session:
        yield session