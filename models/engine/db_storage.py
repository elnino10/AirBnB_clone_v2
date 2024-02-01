#!/usr/bin/python3
"""This module defines a class: `DBStorage`
this serves as database storage engine for the models object
"""
import os  # to import enviroment variables

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from models.base_model import Base

# environment variables
HBNB_MYSQL_USER = os.getenv('HBNB_MYSQL_USER')
HBNB_MYSQL_PWD = os.getenv('HBNB_MYSQL_PWD')
HBNB_MYSQL_HOST = os.getenv('HBNB_MYSQL_HOST', 'localhost')  # locahst if !set
HBNB_MYSQL_DB = os.getenv('HBNB_MYSQL_DB')
HBNB_ENV = os.getenv('HBNB_ENV')


class DBStorage:
    """
    database storage for mapping SQL or database engine
    with objects and performing CRUD operations
    """

    __engine = None
    __session = None

    def __init__(self):
        """public instance method for the intilizing instances"""
        # create engine if all the environment variables are set
        if all(
                var is not None for var in [
                    HBNB_MYSQL_USER,
                    HBNB_MYSQL_PWD,
                    HBNB_MYSQL_HOST,
                    HBNB_MYSQL_DB]
                ):
            db_url = f"mysql+mysqldb://{HBNB_MYSQL_USER}:{HBNB_MYSQL_PWD}"
            db_url += f"@{HBNB_MYSQL_HOST}/{HBNB_MYSQL_DB}"
            # initialzie __engine
            self.__engine = create_engine(db_url, pool_pre_ping=True)

        # drop table when in test environment
        if HBNB_ENV == 'test':
            Base.metadata.drop_all(DBStorage.__engine)

    def all(self, cls=None):
        """
        Queries the current database session (self.__session) all obj
        depending on the class name (i.e arg: cls)
        """
        output = {}
        # Query objects of the specified class
        if cls is not None:
            query_result = self.__session.query(cls).all()
            for obj in query_result:
                key = f"{obj.__class__.__name__}.{obj.id}"
                output[key] = obj
        else:
            # Query all types of obj if cls=None
            for cls_name, cls_obj in Base._decl_class_registry.items():
                if cls_name != 'Base' and isinstance(cls_obj, type):
                    objs = self.__session.query(cls_obj).all()  # get all inst
                    for obj in objs:
                        key = f"{obj.__class__.__name__}.{obj.id}"
                        output[key] = obj
        return output

    def new(self, obj):
        """
        Adds the object to the current database session
        (self.__session)
        """
        self.__session.add(obj)

    def save(self):
        """
        commits all changes of the current db sesssion
        (self.__session)
        """
        self.__session.commit()

    def delete(self, obj=None):
        """Deletes obj from the current db session (self.__session)
        """
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """
        create all tables in the database and recreate the current
        session (self.__session) from the engine (self.__engine)
        """
        # Create all tables in the database
        Base.metadata.create_all(self.__engine)

        # Create a new session and make it scoped
        Session = sessionmaker(bind=self.__engine, expire_on_commit=False)
        self.__session = scoped_session(Session)
