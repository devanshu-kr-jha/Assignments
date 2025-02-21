from flask import Blueprint, jsonify, request
from sqlalchemy import or_, func
from models import User
from db_util import db
from rate_limiter import limiter

api_routes = Blueprint("api_routes", __name__, url_prefix="/api/v1")


# User_controller
@api_routes.route("/test")
@limiter.limit("5/minute")
def test_handler():
    return "user controller route!"


@api_routes.route("/users", methods=["GET"])
@limiter.limit("100/hour;5/minute")
def get_users():
    page = request.args.get("page", default=1, type=int)
    limit = request.args.get("limit", default=5, type=int)
    search = request.args.get("search", default="", type=str).strip()
    sort = request.args.get("sort", default="id", type=str)

    query = db.session.query(User)

    if search:
        query = query.filter(
            or_(
                User.first_name.ilike(f"%{search}%"),
                User.last_name.ilike(f"%{search}%"),
            )
        )

    if sort.startswith("-"):
        sort_field = sort[1:]
        query = query.order_by(getattr(User, sort_field).desc())
    else:
        query = query.order_by(getattr(User, sort).asc())

    paginated_users = query.paginate(page=page, per_page=limit, error_out=False)
    users = paginated_users.items

    # Use 'paginated_user.items' for data and 'paginated_users' for metadata
    data = []
    for user in users:
        data.append(
            {
                "id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "company_name": user.company_name,
                "city": user.city,
                "state": user.state,
                "zip": user.zip,
                "email": user.email,
                "web": user.web,
                "age": user.age,
            }
        )
    return (
        jsonify(
            {
                "data": data,
                "page": paginated_users.page,
                "limit": paginated_users.per_page,
                "total_pages": paginated_users.pages,
                "total_users": paginated_users.total,
            }
        ),
        200,
    )


@api_routes.route("/users/<int:id>", methods=["GET"])
@limiter.limit("5/minute")
def get_user_by_id(id):
    try:
        user = db.session.execute(db.select(User).filter_by(id=id)).scalar_one_or_none()
        if not user:
            return jsonify({"error": "User not found"}), 404

        return (
            jsonify(
                {
                    "data": {
                        "id": user.id,
                        "first_name": user.first_name,
                        "last_name": user.last_name,
                        "company_name": user.company_name,
                        "city": user.city,
                        "state": user.state,
                        "zip": user.zip,
                        "email": user.email,
                        "web": user.web,
                        "age": user.age,
                    }
                }
            ),
            200,
        )

    except Exception as e:
        return jsonify({"error": f"Failed to get user: {str(e)}"}), 500


@api_routes.route("/users", methods=["POST"])
def create_user():
    try:
        data = request.get_json()

        broken_payload = validate_payload(data)
        if broken_payload:
            return jsonify(broken_payload), 400

        unexpected_payload = check_unexpected_fields(data)
        if unexpected_payload:
            return jsonify(unexpected_payload), 400

        new_user = User(
            first_name=data.get("first_name"),
            last_name=data.get("last_name"),
            company_name=data.get("company_name"),
            city=data.get("city"),
            state=data.get("state"),
            zip=data.get("zip"),
            email=data.get("email"),
            web=data.get("web"),
            age=int(data.get("age")),
        )

        db.session.add(new_user)
        db.session.commit()

        return (
            jsonify(
                {
                    "message": "User created successfully",
                    "data": {
                        "id": new_user.id,
                        "first_name": new_user.first_name,
                        "last_name": new_user.last_name,
                        "company_name": new_user.company_name,
                        "city": new_user.city,
                        "state": new_user.state,
                        "zip": new_user.zip,
                        "email": new_user.email,
                        "web": new_user.web,
                        "age": new_user.age,
                    },
                }
            ),
            201,
        )

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Failed to update user: {str(e)}"}), 500


@api_routes.route("/users/<int:id>", methods=["PUT"])
def update_user(id):
    try:
        user = db.session.execute(db.select(User).filter_by(id=id)).scalar_one_or_none()
        if not user:
            return jsonify({"error": "User not found"}), 404

        data = request.get_json()

        broken_payload = validate_payload(data)
        if broken_payload:
            return jsonify(broken_payload), 400

        unexpected_payload = check_unexpected_fields(data)
        if unexpected_payload:
            return jsonify(unexpected_payload), 400

        user.first_name = data.get("first_name")
        user.last_name = data.get("last_name")
        user.company_name = data.get("company_name")
        user.city = data.get("city")
        user.state = data.get("state")
        user.zip = data.get("zip")
        user.email = data.get("email")
        user.web = data.get("web")
        user.age = data.get("age")

        db.session.commit()

        return jsonify({"message": "User updated successfully"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Failed to update user: {str(e)}"}), 500


@api_routes.route("/users/<int:id>", methods=["PATCH"])
def partial_update_user(id):
    try:
        user = db.session.execute(db.select(User).filter_by(id=id)).scalar_one_or_none()
        if not user:
            return jsonify({"error": "User not found"}), 404

        data = request.get_json()

        unexpected_payload = check_unexpected_fields(data)
        if unexpected_payload:
            return jsonify(unexpected_payload), 400

        user.first_name = data.get("first_name", user.first_name)
        user.last_name = data.get("last_name", user.last_name)
        user.company_name = data.get("company_name", user.company_name)
        user.city = data.get("city", user.city)
        user.state = data.get("state", user.state)
        user.zip = data.get("zip", user.zip)
        user.email = data.get("email", user.email)
        user.web = data.get("web", user.web)
        user.age = data.get("age", user.age)

        db.session.commit()

        return jsonify({"message": "User updated successfully"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Failed to update user: {str(e)}"}), 500


@api_routes.route("/users/<int:id>", methods=["DELETE"])
def delete_user(id):
    try:
        user = db.session.execute(db.select(User).filter_by(id=id)).scalar_one_or_none()
        if not user:
            return jsonify({"message": "User not found"}), 404

        db.session.delete(user)
        db.session.commit()

        return jsonify({"message": "User deleted successfully"}), 204

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Failed to delete user: {str(e)}"}), 500


@api_routes.route("/users/summary", methods=["GET"])
@limiter.limit("5/minute")
def get_statistics():
    city_count = (
        db.session.query(User.city, func.count(User.id)).group_by(User.city).all()
    )
    state_count = (
        db.session.query(User.state, func.count(User.id)).group_by(User.state).all()
    )
    avg_age = db.session.query(func.avg(User.age)).scalar()
    max_age = db.session.query(func.max(User.age)).scalar()
    min_age = db.session.query(func.min(User.age)).scalar()

    return (
        jsonify(
            {
                "data": {
                    "count_by_city": {city: count for city, count in city_count},
                    "count_by_state": {state: count for state, count in state_count},
                    "avg_age": round(avg_age, 2) if avg_age else None,
                    "max_age": max_age,
                    "min_age": min_age,
                }
            }
        ),
        200,
    )


# utils
def validate_payload(data):
    required_fields = [
        "first_name",
        "last_name",
        "company_name",
        "city",
        "state",
        "zip",
        "email",
        "web",
        "age",
    ]

    missing_fields = []
    for field in required_fields:
        if not data.get(field):
            missing_fields.append(field)

    if missing_fields:
        return {"error": f'Missing required fields: {", ".join(missing_fields)}'}, 400

    return None


def check_unexpected_fields(data):
    allowed_fields = [
        "first_name",
        "last_name",
        "company_name",
        "city",
        "state",
        "zip",
        "email",
        "web",
        "age",
    ]

    unexpected_fields = set(data) - set(allowed_fields)

    if unexpected_fields:
        return {"error": f'Unexpected fields: {", ".join(unexpected_fields)}'}, 400
    return None
