from db_util import db
from sqlalchemy.orm import Mapped, mapped_column


class User(db.Model):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(nullable=False)
    last_name: Mapped[str]
    company_name: Mapped[str]
    city: Mapped[str]
    state: Mapped[str]
    zip: Mapped[int]
    email: Mapped[str]
    web: Mapped[str]
    age: Mapped[int]


#  {
#         "id": 1,
#         "first_name": "James",
#         "last_name": "Butt",
#         "company_name": "Benton, John B Jr",
#         "city": "New Orleans",
#         "state": "LA",
#         "zip": 70116,
#         "email": "jbutt@gmail.com",
#         "web": "http://www.bentonjohnbjr.com",
#         "age": 70
#     },
