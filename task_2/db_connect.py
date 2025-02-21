from sqlalchemy import create_engine, text

DATABASE_URL = "postgresql://postgres:password@localhost:5432/testDB"
engine = create_engine(DATABASE_URL, echo=True)


with engine.connect() as connection:
    result = connection.execute(text("SELECT'Hello';"))
    print("Connected to PostgreSQL successfully!")
    print(result.all())
