import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
Base = declarative_base()


class User(Base):
        __tablename__ = 'user'
        name = Column(String(250), nullable=False)
        id = Column(Integer, primary_key=True)
        email = Column(String(250), nullable=False)
        picture = Column(String(250))

        @property
        def serialize(self):
            return {
                    'name': self.name,
                    'id': self.id,
                    'email': self.email,
                    'picture': self.picture
            }


class Novel(Base):
        __tablename__ = 'novel'

        id = Column(Integer, primary_key=True)
        name = Column(String(250), nullable=False)
        user_id = Column(Integer, ForeignKey('user.id'))
        user = relationship(User)

        @property
        def serialize(self):
                return{
                        'name': self.name,
                        'id': self.id
                        }


class Book(Base):

        __tablename__ = 'book'
        book_name = Column(String(100), nullable=False)
        id = Column(Integer, primary_key=True)
        author = Column(String(250))
        no_of_pages = Column(String(200))
        genre = Column(String(100))
        book_id = Column(Integer, ForeignKey('book.id'))
        user_id = Column(Integer, ForeignKey('user.id'))
        user = relationship(User)

        @property
        def serialize(self):
                return{
                        'book_name': self.book_name,
                        'id': self.id,
                        'author': self.author,
                        'no_of_pages': self.no_of_pages,
                        'book_id': self.book_id

                }
engine = create_engine('sqlite:///bookdata.db')
Base.metadata.create_all(engine)
