#!/usr/bin/python3
""" Place Module for HBNB project """
from os import getenv
from sqlalchemy import (Column, Float,
                        ForeignKey, Integer,
                        String, Table,
                        inspect)
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base
import models
from models.review import Review
from models.amenity import Amenity

STORAGE_TYPE = getenv("HBNB_TYPE_STORAGE")

if STORAGE_TYPE and STORAGE_TYPE == "db":
    # Define the association table
    place_amenity = Table('place_amenity', Base.metadata,
                          Column('place_id', String(60),
                                 ForeignKey("places.id"),
                                 primary_key=True, nullable=False),
                          Column('amenity_id', String(60),
                                 ForeignKey("amenities.id"),
                                 primary_key=True, nullable=False))


if STORAGE_TYPE and STORAGE_TYPE == "db":
    class Place(BaseModel, Base):
        """ A place to stay
        """
        __tablename__ = "places"
        city_id = Column(String(60), ForeignKey("cities.id"), nullable=False)
        user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
        name = Column(String(128), nullable=False)
        description = Column(String(1024))
        number_rooms = Column(Integer, default=0)
        number_bathrooms = Column(Integer, default=0)
        max_guest = Column(Integer, default=0)
        price_by_night = Column(Integer, default=0)
        latitude = Column(Float)
        longitude = Column(Float)
        if STORAGE_TYPE == 'db':
            reviews = relationship("Review", backref="place",
                                   cascade="all, delete-orphan")
            amenities = relationship("Amenity", secondary="place_amenity",
                                     viewonly=False)

        @classmethod
        def __declare_last__(cls):
            """
            Hook called by SQLAlchemy after all models have been generated.
            """
            # Suppress SAWarning about expected row deletions
            mapper = inspect(cls)
            mapper.confirm_deleted_rows = False

if not STORAGE_TYPE or STORAGE_TYPE != 'db':
    class Place(BaseModel):
        """ A place to stay
        """
        city_id = ''
        user_id = ''
        name = ''
        description = ''
        number_rooms = 0
        number_bathrooms = 0
        max_guest = 0
        price_by_night = 0
        latitude = 0.0
        longitude = 0.0
        amenity_ids = []

        def __init__(self, *args, **kwargs):
            """initializes Place"""
            super().__init__(*args, **kwargs)

        @property
        def reviews(self):
            """Get a list of all linked Reviews."""
            all_reviews = list(models.storage.all(Review).values())
            review_list = [review for review in all_reviews if
                           review.place_id == self.id]
            return review_list

        @property
        def amenities(self):
            """Get/set linked Amenities."""
            all_am = list(models.storage.all(Amenity).values())
            amenity_list = [a for a in all_am if a.id in self.amenity_ids]
            return amenity_list

        @amenities.setter
        def amenities(self, value):
            """
            Appends amenities id to amenity_ids list
            """
            if type(value) is Amenity:
                self.amenity_ids.append(value.id)
