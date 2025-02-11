from datetime import datetime
from sqlalchemy import Date, cast, create_engine, Column, Integer, String, Text, Numeric, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from flask_sqlalchemy import SQLAlchemy
import os

# Database URL (replace with your actual credentials)
# database_path = os.getenv('DATABASE_URL', $env:DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/postgres")
database_path = os.environ['DATABASE_URL']

# Create a new SQLAlchemy engine instance
engine = create_engine(database_path, echo=True)

# Base class for declarative models
Base = declarative_base()

# Initialize SQLAlchemy
db = SQLAlchemy()

# Define the Movie model
class Movie(Base):
    __tablename__ = 'movies'
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    release_date = Column(String, nullable=False)
    actors = relationship('Actor', back_populates='movie')

    def __repr__(self):
        return f'<Movie(title={self.title}, release_date={self.release_date})>'

# Define the Actor model
class Actor(Base):
    __tablename__ = 'actors'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String, nullable=False)
    movie_id = Column(Integer, ForeignKey('movies.id'), nullable=True)
    movie = relationship('Movie', back_populates='actors')

    def __repr__(self):
        return f'<Actor(name={self.name}, age={self.age}, gender={self.gender})>'

# Create all tables
def create_tables():
    Base.metadata.create_all(engine)
    print("Tables created")

# Insert sample data
def insert_sample_data():
    Session = sessionmaker(bind=engine)
    session = Session()
    
    movie1 = Movie(
        title="Inception", 
        release_date=cast(datetime.strptime("2010-07-16", "%Y-%m-%d").date(), Date)
    )
    movie2 = Movie(
        title="Interstellar", 
        release_date=cast(datetime.strptime("2014-11-07", "%Y-%m-%d").date(), Date)
    )
    session.add_all([movie1, movie2])
    session.commit()
    
    actor1 = Actor(name="Leonardo DiCaprio", age=47, gender="Male", movie=movie1)
    actor2 = Actor(name="Matthew McConaughey", age=54, gender="Male", movie=movie2)
    actor3 = Actor(name="Anne Hathaway", age=41, gender="Female", movie=movie2)
    
    session.add_all([actor1, actor2, actor3])
    session.commit()
    
    print("Sample data inserted")

if __name__ == '__main__':
    create_tables()
    insert_sample_data()
