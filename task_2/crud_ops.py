from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from data_models import User, Movie, Review
from db_connect import engine
import argparse

session = Session(engine)


def create_user(id: int, name: str, email: str) -> None:
    new_user = User(id=id, name=name, email=email)
    try:
        session.add(new_user)
        session.commit()

        print(f"User: '{name}' added successfully.")
    except SQLAlchemyError:
        session.rollback()
        print(f"Error creating new user with Id:{id}")


def add_movie(id: int, title: str, genre: str, release_year: int) -> None:
    new_movie = Movie(id=id, title=title, genre=genre, release_year=release_year)
    try:
        session.add(new_movie)
        session.commit()

        print(f"Movie: {title} added successfully.")
    except SQLAlchemyError:
        session.rollback()
        print(f"Error adding movie {title}")


def add_review(
    id: int, user_id: int, movie_id: int, rating: int, review_text: str
) -> None:
    if not user_exists(user_id):
        print(f"User with ID:{user_id} does not exist.")
        return
    if not movie_exists(movie_id):
        print(f"Movie with ID:{movie_id} does not exist.")
        return

    existing_review = (
        session.query(Review)
        .filter(Review.user_id == user_id, Review.movie_id == movie_id)
        .first()
    )
    if existing_review:
        print(
            f"User: {user_id} has already reviewed Movie: {movie_id}. Only single review per movie is allowed for any user."
        )
        return

    user = session.query(User).get(user_id)
    movie = session.query(Movie).get(movie_id)

    new_review = Review(
        id=id,
        user_id=user_id,
        movie_id=movie_id,
        rating=rating,
        review_text=review_text,
    )
    try:
        session.add(new_review)
        session.commit()

        print(
            f"Review for movie '{movie.title}' by user '{user.name}' added successfully."
        )
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Error adding review: {e}")


def get_review_by_movie(movie_title: str) -> None:
    reviews = session.query(Review).join(Movie).filter(Movie.title == movie_title).all()

    for review in reviews:
        print(
            f"Movie: {movie_title} | Rating: {review.rating} | Review: {review.review_text}"
        )


def get_review_by_user(user_id: int):
    if not user_exists(user_id):
        print(f"User with ID:{user_id} does not exist.")
        return

    reviews = (
        session.query(Review, Movie.title)
        .join(Movie)
        .filter(Review.user_id == user_id)
        .all()
    )

    for review, movie_title in reviews:
        print(
            f"User ID: {user_id} | Movie: {movie_title} | Rating: {review.rating} | Review: {review.review_text}"
        )


def update_review_rating(review_id: int, new_rating: int):
    if not validate_rating_range(new_rating):
        return

    if not review_exists(review_id):
        print(f"Review with ID:{review_id} does not exist.")
        return

    try:
        session.query(Review).filter(Review.id == review_id).update(
            {"rating": new_rating}
        )
        session.commit()

        print(f"Successfully updated review ID:{review_id} to new rating: {new_rating}")
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Error updating review rating: {e}")


def remove_review(review_id: int):
    if not review_exists(review_id):
        print(f"Review with ID:{review_id} does not exist.")
        return
    try:
        review = session.query(Review).filter(Review.id == review_id).first()
        session.delete(review)
        session.commit()

        print(f"Review with ID:{review_id} has been removed.")
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Error removing review: {e}")


# Utils
def review_exists(review_id: int) -> bool:
    return session.query(Review.id).filter(Review.id == review_id).first() is not None


def validate_rating_range(rating: int) -> bool:
    if rating < 1 or rating > 5:
        print("Invalid rating! Please enter a value between 1 and 5.")
        return False
    return True


def user_exists(user_id: int) -> bool:
    return session.query(User.id).filter(User.id == user_id).first() is not None


def movie_exists(movie_id: int) -> bool:
    return session.query(Movie.id).filter(Movie.id == movie_id).first() is not None


# Test relation integrity
def remove_movie(movie_id: int) -> None:
    movie = session.query(Movie).filter(Movie.id == movie_id).first()
    session.delete(movie)
    session.commit()

    print(f"Movie with ID:{movie_id} has been removed.")


def remove_user(user_id: int) -> None:
    user = session.query(User).filter(User.id == user_id).first()

    session.delete(user)
    session.commit()

    print(f"User with ID:{user_id} has been removed.")


def main():
    # create_user(2, 'David Brown', 'david.brown@example.com')

    # add_movie(3, 'The Godfather', 'Crime', 1972)

    # add_review(2,1,3,5,'An epic masterpiece that defines cinema. A timeless classic')

    # get_review_by_movie('The Dark Knight')

    # get_review_by_user(1)

    # update_review_rating(2,4)

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command")

    user_parser = subparsers.add_parser("create_user")
    user_parser.add_argument("--id", type=int, required=True)
    user_parser.add_argument("--name", type=str, required=True)
    user_parser.add_argument("--email", type=str, required=True)

    review_parser = subparsers.add_parser("review_by_movie")
    review_parser.add_argument("--title", type=str, required=True)

    args = parser.parse_args()

    if args.command == "add_user":
        create_user(args.id, args.name, args.email)
    elif args.command == "review_by_movie":
        get_review_by_movie(args.title)


if __name__ == "__main__":
    main()
