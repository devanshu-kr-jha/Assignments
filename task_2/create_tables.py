from data_models import Base
from db_connect import engine

Base.metadata.create_all(bind=engine)
