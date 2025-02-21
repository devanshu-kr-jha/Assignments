import json
from db_util import db
from models import User


path_to_file = "users.json"


def populate_db(path_to_file):
    try:
        with open(path_to_file, "r") as fp:
            user_list = json.load(fp)

            for user in user_list:
                new_user = User(
                    first_name=user["first_name"],
                    last_name=user.get("last_name"),
                    company_name=user.get("company_name"),
                    city=user.get("city"),
                    state=user.get("state"),
                    zip=user.get("zip"),
                    email=user["email"],
                    web=user.get("web"),
                    age=user.get("age"),
                )

                db.session.add(new_user)
                db.session.commit()

            print("All records from users.json added successfully to db")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        db.session.rollback()
