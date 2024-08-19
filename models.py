from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

db=SQLAlchemy(model_class=Base)

class Movie(Base):
    __tablename__= 'movies'
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(db.String(255))
    director: Mapped[str] = mapped_column(db.String(255))
    year: Mapped[int] = mapped_column(db.Integer)
    # genres: Mapped['MovieGenre'] = db.relationship(back_populates='movie')


class Genre(Base):
    __tablename__= 'genres'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(255))
    # movies: Mapped['MovieGenre'] = db.relationship(back_populates='genres')

# class MovieGenre(Base):
#     __tablename__ = 'movie_genre'
#     movie_id: Mapped[int] = mapped_column(db.ForeignKey('movies.id'), primary_key=True)
#     genre_id: Mapped[int] = mapped_column(db.ForeignKey('genre.id'), primary_key=True)
#     movie: Mapped['Movie'] = db.relationship(back_populates='movies')
#     genre: Mapped['Genre'] = db.relationship(back_populates='genres')
