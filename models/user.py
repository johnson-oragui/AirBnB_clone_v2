#!/usr/bin/python3
"""Defines the User class."""
from os import getenv
from models.base_model import Base
from models.base_model import BaseModel
from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy.orm import relationship


if getenv("HBNB_TYPE_STORAGE") and getenv("HBNB_TYPE_STORAGE") == "db":
    class User(BaseModel, Base):
        """Represents a user for a MySQL database.

        Inherits from SQLAlchemy Base and links to the MySQL table users.

        Attributes:
            __tablename__ (str): The name of the MySQL table to store users.
            email: (sqlalchemy String): The user's email address.
            password (sqlalchemy String): The user's password.
            first_name (sqlalchemy String): The user's first name.
            last_name (sqlalchemy String): The user's last name.
            places (sqlalchemy relationship): The User-Place relationship.
            reviews (sqlalchemy relationship): The User-Review relationship.
        """
        __tablename__ = "users"
        email = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        first_name = Column(String(128))
        last_name = Column(String(128))
        places = relationship("Place", backref="user",
                              cascade="all, delete-orphan")
        reviews = relationship("Review", backref="user", cascade="delete")
else:
    class User(BaseModel):
        """This class defines a user by various attributes"""
        email = ''
        password = ''
        first_name = ''
        last_name = ''
