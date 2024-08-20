import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType
from models import db
import models
from sqlalchemy.orm import Session


class Movie(SQLAlchemyObjectType):
    class Meta:
        model = models.Movie #This is mapping to the movie model in our models.py

class Genre(SQLAlchemyObjectType):
    class Meta:
        model= models.Genre

class Query(graphene.ObjectType):
    movies = graphene.List(Movie)
    genres = graphene.List(Genre)

    def resolve_movies(self, info): # Resolver
        return db.session.execute(db.select(models.Movie)).scalars()
    
    def resolve_genres(self, info):
        return db.session.execute(db.select(models.Genre)).scalars()
    
class AddGenre(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        
    
    genre = graphene.Field(Genre)

    def mutate(self, info, name):
        with Session(db.engine) as session:
            with session.begin():
                genre = models.Genre(name=name)
                
                
                session.add(genre)

            session.refresh(genre)
            return AddGenre(genre=genre)
class UpdateGenre(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        title = graphene.String(required=True)
        director = graphene.String(required=True)
        year = graphene.Int(required=True)
        genre_ids = graphene.List(graphene.Int, required=True)

    genre = graphene.Field(Genre)

    def mutate(self, info, id, name):
        with Session(db.engine) as session:
            with session.begin():
                genre = session.execute(db.select(models.Genre).where(models.Genre.id == id)).scalars().first()
                if genre:
                    genre.name= name
                else:
                    return None
            session.refresh(genre)
            return UpdateGenre(genre=genre)
        

class DeleteGenre(graphene.Mutation):
    class Arguments:
        id=graphene.Int(required=True)

    genre = graphene.Field(Genre)

    def mutate(self, info, id):
        with Session(db.engine) as session:
            with session.begin():
                genre = session.execute(db.select(models.Genre).where(models.Genre.id==id)).scalars().first()
                if genre:
                    session.delete(genre)
                else:
                    return None
            session.refresh(genre)
            return DeleteGenre(genre=genre)

        
class AddMovie(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        director = graphene.String(required=True)
        year = graphene.Int(required=True)
        genre_ids = graphene.List(graphene.Int, required=True)

    movie = graphene.Field(Movie)

    def mutate(self, info, title, director, year, genre_ids):
        with Session(db.engine) as session:
            with session.begin():
                movie = models.Movie(title=title, director=director, year=year)
                genres = session.query(models.Genre).filter(models.Genre.id.in_(genre_ids)).all()
                movie.genres.extend(genres)
                session.add(movie)

            session.refresh(movie)
            return AddMovie(movie=movie)
        
class UpdateMovie(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        title = graphene.String(required=True)
        director = graphene.String(required=True)
        year = graphene.Int(required=True)
        genre_ids = graphene.List(graphene.Int, required=True)

    movie = graphene.Field(Movie)

    def mutate(self, info, id, title, director, year, genre_ids):
        with Session(db.engine) as session:
            with session.begin():
                movie = session.execute(db.select(models.Movie).where(models.Movie.id == id)).scalars().first()
                if movie:
                    movie.title = title
                    movie.director = director
                    movie.year = year
                    genres = session.query(models.Genre).filter(models.Genre.id.in_(genre_ids)).all()
                    movie.genres = genres
                else:
                    return None
            session.refresh(movie)
            return UpdateMovie(movie=movie)
        
class DeleteMovie(graphene.Mutation):
    class Arguments:
        id=graphene.Int(required=True)

    movie = graphene.Field(Movie)

    def mutate(self, info, id):
        with Session(db.engine) as session:
            with session.begin():
                movie = session.execute(db.select(models.Movie).where(models.Movie.id==id)).scalars().first()
                if movie:
                    session.delete(movie)
                else:
                    return None
            session.refresh(movie)
            return DeleteMovie(movie=movie)


class Mutation(graphene.ObjectType):
    create_movie = AddMovie.Field()
    update_movie = UpdateMovie.Field()
    delete_movie = DeleteMovie.Field()
    create_genre =AddGenre.Field()
    update_genre= UpdateGenre.Field()
    delete_genre = DeleteGenre.Field()