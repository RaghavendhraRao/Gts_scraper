import os
import yaml
from model import Base
import sqlalchemy
from sqlalchemy import create_engine
from model import metadata
import logging.config


def create_db_tables():
    CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))
    os.chdir(CURRENT_PATH)

    INITIALIZEYAML_OBJ = None

    with open('instance_settings.yaml', 'r') as yaml_file:
        try:
            INITIALIZEYAML_OBJ = yaml.safe_load(yaml_file)
        except Exception as e:
            logging.info("exception with yaml")

    HOST = INITIALIZEYAML_OBJ.get('HOST')
    DB_USERNAME = INITIALIZEYAML_OBJ.get('DB_USERNAME')
    DB_PASSWORD = INITIALIZEYAML_OBJ.get('DB_PASSWORD')
    DB_NAME = INITIALIZEYAML_OBJ.get('DB_NAME')

    DB_URL = 'mariadb+mariadbconnector://' + DB_USERNAME + ':' + DB_PASSWORD + '@' + HOST + '/' + DB_NAME + '?charset=utf8mb4'
    engine = sqlalchemy.create_engine(DB_URL)

    # Create all tables
    Base.metadata.create_all(engine)
    logging.info("Database connected")
    print("Database connected")

    return engine


if __name__ == '__main__':
    engine = create_db_tables()
