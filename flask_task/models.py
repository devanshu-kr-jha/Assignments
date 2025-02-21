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

    # def __init__(self, first_name, last_name, company_name, city, state, zip, email, web, age):
    #     self.first_name = first_name
    #     self.last_name = last_name
    #     self.company_name = company_name
    #     self.city = city
    #     self.state = state
    #     self.zip = zip
    #     self.email = email
    #     self.web = web
    #     self.age = age


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
