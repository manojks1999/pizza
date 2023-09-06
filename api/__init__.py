# import timedelta
from datetime import timedelta, datetime
import os
# import config
import api.config as config

# import flask
from flask import Flask, has_request_context, request as req

# import cors
# from flask_cors import CORS

# db
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Table, Column, Integer, JSON, MetaData, VARCHAR
import sqlalchemy
import pymysql

# import db conn. retrying class
from api.db import RetryingQuery
from .utils import make_celery


# global db objects
engine = None
db_session = None

def create_app(environment):
    """
    Initialize flask WSGI application with a config object.

    params:
        - config_object: flask configuration object (class)
    """
    try:
        config_object = config.Config
        # create Flask object
        app = Flask(__name__, instance_relative_config=False)
        # create Flask object
        app = Flask(__name__, instance_relative_config=False)
        app.config["CELERY_CONFIG"] = {"broker_url": "redis://redis", "result_backend": "redis://redis"}
        global engine
        engine = create_engine(
            "mysql+pymysql://root:root@db:3306/local_db",
            # "mysql+pymysql://freedb_sql12643999:z&g?k2v&Wdn87M?@sql.freedb.tech:3306/freedb_local_db",
            echo=True,
            pool_pre_ping=True
        )
        # tables  = sqlalchemy.inspect(engine).get_table_names()
        # print(tables)
        # itemTable = 'items'
        # ordersTable = 'orders'
        # if not tables:  # If table don't exist, Create.
        #     metadata = MetaData()
        #     # Create a table with the appropriate Columns
        #     Table(itemTable, metadata,
        #         Column('id', VARCHAR, primary_key=True, nullable=False), 
        #         Column('name', VARCHAR),
        #         Column('price', Integer))
        #     # Create a table with the appropriate Columns

        #     Table(ordersTable, metadata,
        #         Column('id', VARCHAR, primary_key=True, nullable=False), 
        #         Column('quantity', Integer),
        #         Column('total_price', float),
        #         Column('item', JSON))
        #     # Implement the creation
        #     metadata.create_all(engine)
        # intialize database session (verbose SQL operations can be activated here)
        Session = scoped_session(sessionmaker(bind=engine))
        # get session
        global db_session
        # create session
        db_session = Session()
        db_session.connection(
            execution_options={
                "schema_translate_map": {"development": "development"}
            }
        )
        # get declarative base
        global Base
        # initialize declarative base
        Base = declarative_base()
        from .schema import Items, Orders
        # bind engine with declarative base
        Base.metadata.bind = engine
        celery = make_celery(app)
        celery.set_default()
        # Base.metadata.create_all(engine)
        # pass application context
        with app.app_context():
            # import blueprints
            from api.api import apis_blueprint, main_blueprint
            app.register_blueprint(apis_blueprint)
            app.register_blueprint(main_blueprint)
            return app, celery
    except Exception as e:
        print("error", e)
        return None
