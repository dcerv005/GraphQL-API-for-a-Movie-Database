import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType
from models import Movie as MovieModel, db
from models import Genre as GenreModel
from sqlalchemy.orm import Session


class Movie(SQLAlchemyObjectType):
    class Meta:
        model = MovieModel #This is mapping to the movie model in our models.py

class Genre(SQLAlchemyObjectType):
    class Meta:
        genre_model= GenreModel

class Query(graphene.ObjectType):
    movies = graphene.List(Movie)
    genres = graphene.List(Genre)

    def resolve_movies(self, info): # Resolver
        return db.session.execute(db.select(MovieModel)).scalars()
    
    def resolve_genres(self,info):
        return db.session.execute(db.select(GenreModel)).scalars()
    
class AddMovie(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        director = graphene.String(required=True)
        year = graphene.Int(required=True)

    movie = graphene.Field(Movie)

    def mutate(self, info, title, director, year):
        with Session(db.engine) as session:
            with session.begin():
                movie = MovieModel(title=title, director=director, year=year)
                session.add(movie)

            session.refresh(movie)
            return AddMovie(movie=movie)
        
class UpdateMovie(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        title = graphene.String(required=True)
        director = graphene.String(required=True)
        year = graphene.Int(required=True)

    movie = graphene.Field(Movie)

    def mutate(self, info, id, title, director, year):
        with Session(db.engine) as session:
            with session.begin():
                movie = session.execute(db.select(MovieModel).where(MovieModel.id == id)).scalars().first()
                if movie:
                    movie.title = title
                    movie.director = director
                    movie.year = year
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
                movie = session.execute(db.select(MovieModel).where(MovieModel.id==id)).scalars().first()
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