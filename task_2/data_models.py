from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String, CheckConstraint


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)

    reviews = relationship(
        "Review", back_populates="user", cascade="all, delete-orphan"
    )


class Movie(Base):
    __tablename__ = "movies"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False)
    genre: Mapped[str] = mapped_column(String(50), nullable=True)
    release_year: Mapped[int] = mapped_column(nullable=True)

    reviews = relationship(
        "Review", back_populates="movie", cascade="all, delete-orphan"
    )


class Review(Base):
    __tablename__ = "reviews"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    movie_id: Mapped[int] = mapped_column(
        ForeignKey("movies.id", ondelete="CASCADE"), nullable=False
    )
    rating: Mapped[int] = mapped_column(nullable=False)

    review_text: Mapped[str] = mapped_column(nullable=True)

    user = relationship("User", back_populates="reviews")
    movie = relationship("Movie", back_populates="reviews")

    __table_args__ = (
        CheckConstraint("rating BETWEEN 1 AND 5", name="check_rating_range"),
    )
