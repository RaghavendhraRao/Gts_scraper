import hashlib
import os
import time
import re
from bs4 import BeautifulSoup
import requests
import yaml
from selectorlib import Extractor
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from random import choice
import logging.config
import html_text
from random import choice
from model import User, Institution, Area, Degree, Location, Inst_param_value, Inst_param_group, Program, \
    Requirement_group, Term, Requirement, Degree_level, Program_area, Program_location, Requirement_term, Department, \
    Course, Course_gs_category, Course_additional_detail, Gs_category, Notes, Requirement_variable, App_param_group, \
    App_param_value, Graduate_req_category, Admission_req, Rqmt_group_rqmt_category, Institution_location, \
    Program_college, \
    Rqmt_group_college, Rqmt_group_location, Course_college

from sqlalchemy.orm import sessionmaker
from model import Base
from sqlalchemy import inspect, select
import uuid
from selenium.webdriver.common.by import By
import logging.config
import initialize_db
from datetime import datetime
from model import Base
from furl import furl
from sqlalchemy import create_engine
import html_text

with open(r'logging_config_template.yaml', 'r') as f:
    config = yaml.safe_load(f.read())
    config['handlers']['all']['filename'] = os.path.join(
        config['handlers']['all']['filename'] + "bilgi_scrape" + ".log")
    logging.config.dictConfig(config)
logger = logging.getLogger(__name__)

with open(r'bilgi_selectors.yaml', 'r') as stream:
    try:
        yaml_obj = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        logger.info("Exception raised while opening selectors.yaml file", exc)
        raise

#Global variables
check_course_pagination_links = []

# create database tables
engine = initialize_db.create_db_tables()
logging.info("tables created in the database.")

# create a new session and connection
conn = engine.connect()
Session = sessionmaker(bind=engine)
session = Session()


# check table exist in the database.
def table_exists(engine, name):
    ins = inspect(engine)
    ret = ins.dialect.has_table(engine.connect(), name)
    logger.info('Table "{}" exists: {} %s'.format(name, ret))
    return ret


def extract_data_using_selector_lib(new_soup, typo, Website_URL):
    try:
        a = ext.__dict__
        b = a['config'][Website_URL][typo]
        c = Extractor(b)
        data = c.extract(str(new_soup))
        return data
    except Exception as e:
        print(e)


def prepare_soup(Website_URL):
    driver.get(Website_URL)
    time.sleep(2)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    return soup


def convert_list_to_str(lst):
    return " ".join(lst)


def get_tuple_id(id):
    for i in id:
        return i

# calling master data before driver starts
# inserting user and app_group data
def master_data_user():
    try:
        if not table_exists(engine, 'user'):
            Base.metadata.tables['user'].create(engine)
            logger.info("table created")
        logger.info("Inserting into user table")
        count = session.query(User.external_id).where(User.email == "admin@cintana.com").all()
        if len(count) > 0:
            logger.info("duplicate record in user table")
        else:
            user_table = [
                User(str(uuid.uuid4()), hashlib.md5("admin@cintana.com".encode('utf-8')).hexdigest(), "Admin", None,
                     None,
                     "admin@cintana.com", '$2a$10$E9/AjpcuEkLUEtC3XIRp1uqHsdve3Ngs2hOJY.u4oNWsX6BUMyk72', None, None,
                     datetime.now(), None, datetime.now(), None),
                User(str(uuid.uuid4()), hashlib.md5("ediez@cintana.com".encode('utf-8')).hexdigest(), "Emiliano", None,
                     'Diez',
                     "ediez@cintana.com", '$2a$10$E9/AjpcuEkLUEtC3XIRp1uqHsdve3Ngs2hOJY.u4oNWsX6BUMyk72', None, None,
                     datetime.now(), None, datetime.now(), None)
            ]
            session.add_all(user_table)  # persists data
            session.commit()
            logger.info("user table data inserted")
    except Exception as e:
        session.rollback()
        logger.info("Error raosed in user table as: %s" % e)
        pass


def master_data_app_param_group():
    try:
        if not table_exists(engine, 'app_param_group'):
            Base.metadata.tables['app_param_group'].create(engine)
            logger.info("table created")
        logger.info("Inserting into app_param_group")
        count = session.query(App_param_group.name).where(App_param_group.name == 'TRANSFER_DIRECTION').all()
        if len(count) > 0:
            logger.info("duplicate record in App_param_group table")
        else:
            app_param_group = [App_param_group(1, 'TRANSFER_DIRECTION', 'transferDirection', 1),
                               App_param_group(2, 'GLOBAL_PROGRAM_REQUEST_STATUS',
                                               'it will denotes the requested global program status', 1),
                               App_param_group(3, 'GLOBAL_PROGRAM_MAP_STATUS',
                                               'it will denotes the requested global program map status', 1),
                               App_param_group(4, 'GLOBAL_PROGRAM_REQUIREMENT_BUNDLE_STATUS',
                                               'it will denotes the requested global program mapped requirement bundle status',
                                               1),
                               App_param_group(5, 'PROGRAM_STATUS', 'it will denotes the program status', 1)
                               ]
            session.add_all(app_param_group)
            session.commit()
            logger.info("app_param_group data inserted")
    except Exception as e:
        session.rollback()
        logger.info("error in inserting app_param_group")
        pass


def master_data_app_param_value():
    try:
        if not table_exists(engine, 'app_param_value'):
            Base.metadata.tables['app_param_value'].create(engine)
            logger.info("table created")
        logger.info("Inserting into app_param_value table")
        count = session.query(App_param_value.name).where(App_param_value.name == 'provider-to-subscriber').all()
        if len(count) > 0:
            logger.info("duplicate records in App_param_value table")
        else:
            app_param_value = [App_param_value(1, 1, 'provider-to-subscriber', None, None, 1),
                               App_param_value(2, 1, 'subscriber-to-provider', None, None, 1),
                               App_param_value(3, 1, 'no transfer', None, None, 1),
                               App_param_value(4, 2, 'Mapping Pending', None, None, 1),
                               App_param_value(5, 2, 'Mapping In Progress', None, None, 1),
                               App_param_value(6, 2, 'Approval Pending', None, None, 1),
                               App_param_value(7, 2, 'Approved', None, None, 1),
                               App_param_value(8, 2, 'Rejected', None, None, 1),
                               App_param_value(9, 3, 'Mapping Pending', None, None, 1),
                               App_param_value(10, 3, 'Mapping In Progress', None, None, 1),
                               App_param_value(11, 3, 'Approval Pending', None, None, 1),
                               App_param_value(12, 3, 'Approved', None, None, 1),
                               App_param_value(13, 3, 'Rejected', None, None, 1),
                               App_param_value(14, 4, 'In Progress', None, None, 1),
                               App_param_value(15, 4, 'Approval Pending', None, None, 1),
                               App_param_value(16, 4, 'Approved', None, None, 1),
                               App_param_value(17, 4, 'Rejected', None, None, 1),
                               App_param_value(18, 4, 'Not Reveiwed', None, None, 1),
                               App_param_value(19, 5, 'Articulation Available', None, None, 1),
                               App_param_value(20, 5, 'Articulation Unavailable', None, None, 1),
                               App_param_value(21, 5, 'Articulation In Process', None, None, 1),
                               App_param_value(22, 5, 'Articulation Approved', None, None, 1),
                               App_param_value(23, 5, 'Articulation Rejected', None, None, 1)]
            session.add_all(app_param_value)
            session.commit()
            logger.info("data inserted into app_param_value")
    except Exception as e:
        session.rollback()
        logger.info("error in inserting app_param_value")
        pass


def master_data_inst_param_group():
    try:
        if not table_exists(engine, 'inst_param_group'):
            Base.metadata.tables['inst_param_group'].create(engine)
            logger.info("table created")
        logger.info("Inserting into inst_param_group table")
        logger.info("inserting data into inst_param_group,")
        count = session.query(Inst_param_group.name).where(Inst_param_group.name == 'PROGRAM_LEVEL').all()
        if len(count) > 0:
            logger.info("duplicate records found in Inst_param_group")
        else:
            inst_param_group = [Inst_param_group(1, 'PROGRAM_LEVEL', 'denotes the level of program', 1),
                                Inst_param_group(2, 'DEGREE_LEVEL', None, 1),
                                Inst_param_group(3, 'MATH_INTENSITY', None, 1),
                                Inst_param_group(4, 'COURSE_LEVEL', None, 1),
                                ]
            session.add_all(inst_param_group)
            session.commit()
            logger.info("inst_param_group data inserted")
    except Exception as e:
        session.rollback()
        logger.info("error in inserting Inst_param_group")
        pass


# insering data
logger.info("calling user master_data")
master_data_user()
logger.info("calling app_param_group master_data")
master_data_app_param_group()
logger.info("calling app_param_value master_data")
master_data_app_param_value()
logger.info("calling inst_param_group master_data")
master_data_inst_param_group()


desktop_agents = \
    ['Mozilla/5.0(Windows NT 6.1; WOW64) AppleWebKit/537.36(KHTML, like Gecko) '
     'Chrome/54.0.2840.99 Safari/537.36',
     'Mozilla/5.0(Windows NT 10.0; WOW64) AppleWebKit/537.36(KHTML, like Gecko) '
     'Chrome/54.0.2840.99 Safari/537.36',
     'Mozilla/5.0(Windows NT 10.0; Win64; x64) AppleWebKit/537.36(KHTML, like Gecko) '
     'Chrome/54.0.2840.99 Safari/537.36',
     'Mozilla/5.0(Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/602.2.14(KHTML, like Gecko) '
     'Version/10.0.1 Safari/602.2.14',
     'Mozilla/5.0(Windows NT 10.0; WOW64) AppleWebKit/537.36(KHTML, like Gecko) '
     'Chrome/54.0.2840.71 Safari/537.36',
     'Mozilla/5.0(Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36(KHTML, like Gecko) '
     'Chrome/54.0.2840.98 Safari/537.36',
     'Mozilla/5.0(Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36(KHTML, like Gecko) '
     'Chrome/54.0.2840.98 Safari/537.36',
     'Mozilla/5.0(Windows NT 6.1; WOW64) AppleWebKit/537.36(KHTML, like Gecko) '
     'Chrome/54.0.2840.71 Safari/537.36',
     'Mozilla/5.0(Windows NT 6.1; Win64; x64) AppleWebKit/537.36(KHTML, like Gecko) '
     'Chrome/54.[;;[;0.2840.99 Safari/537.36',
     'Mozilla/5.0(Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0']

options = Options()
options.headless = False
s = Service('C:/Program Files/geckodriver-v0.29.1-win64/geckodriver.exe')
# executable_path='/data/softwares/geckodriver'
# service=s
driver = webdriver.Firefox(options=options, service=s)
logger.info("Driver started ----> Headless")

userAgent = choice(desktop_agents)
driver.addheaders = [('User-Agent', userAgent),
                     ('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'),
                     ('Accept-Charset', 'ISO-8859-1,utf-8;q=0.7,*;q=0.3'),
                     ('Accept-Encoding', 'none'),
                     ('Accept-Language', 'en-US,en;q=0.8'),
                     ('Connection', 'keep-alive')]

ext = Extractor.from_yaml_file('bilgi_selectors.yaml')
CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))
os.chdir(CURRENT_PATH)
os.chdir('../..')

# Global parameters reffered in other inserting tables.
created_by = session.query(User.id).filter(User.email == 'admin@cintana.com').one()
created_at = datetime.now()
updated_by = session.query(User.id).filter(User.email == 'admin@cintana.com').one()
updated_at = datetime.now()


def insert_into_university_institution(university_name):  # inserting parent colleges into institution
    logger.info("inserting parent data into Institution table")
    global parent_id
    try:
        if not table_exists(engine, 'institution'):
            Base.metadata.tables['institution'].create(engine)
            logger.info("table created")
        uniq_id = str(uuid.uuid4())
        external_id = hashlib.md5(university_name.encode('utf-8')).hexdigest()  # ('ascii', 'ignore')
        count = session.query(Institution.external_id).where(Institution.external_id == external_id).all()
        if len(count) > 0:
            logger.info("Duplicate record found")
        else:
            institution_table = Institution(uniq_id, external_id, university_name, 'IBU', None, 'University', None,
                                            datetime.now(), created_by[0], datetime.now(), updated_by[0])
            session.add(institution_table)  # persists data
            session.commit()  # commit and close session
            logger.info("Parent-institution data inserted")
    except Exception as e:
        session.rollback()
        logger.debug("Exception raised insert_into_institution-parent() : %s" % e)
        pass
    session.close()


def master_data_into_inst_param_values(university_name):
    global inst_parent_id
    try:
        if not table_exists(engine, 'inst_param_value'):
            Base.metadata.tables['inst_param_value'].create(engine)
            logger.info("table created")
        logger.info("inserting into inst_param_value table")
        logger.info("inserting into inst_param_value")
        try:
            inst_parent_id = session.query(Institution.id).filter_by(name=university_name).one()
        except Exception as e:
            logger.debug("Exception raised:No id found in insert_colleges_into_institution(): %s" % e)
            pass
        sub_query = session.query(Institution.id).where(Institution.name == university_name).one()
        count = session.query(Inst_param_value.name).where(Inst_param_value.name == 'Graduate').where(
            Inst_param_value.inst_id.in_(sub_query)).all()
        if len(count) > 0:
            logger.info("duplicate records found in Inst_param_value")
        else:
            inst_param_value = [Inst_param_value(1, 1, inst_parent_id[0], 'Graduate', None, 1, 1),
                                Inst_param_value(2, 1, inst_parent_id[0], 'Undergraduate', None, 1, 1),
                                Inst_param_value(3, 1, inst_parent_id[0], 'Undergraduate Minors and Certificates', None,
                                                 1, 1),
                                Inst_param_value(4, 2, inst_parent_id[0], 'Master\'s Degree', None, 1, 1),
                                Inst_param_value(5, 2, inst_parent_id[0], 'Doctoral Degree', None, 1, 1),
                                Inst_param_value(6, 2, inst_parent_id[0], 'certificate', None, 1, 1),
                                Inst_param_value(7, 2, inst_parent_id[0], 'Bachelor\'s Degree', None, 1, 1),
                                Inst_param_value(8, 3, inst_parent_id[0], 'General', None, 1, 1),
                                Inst_param_value(9, 3, inst_parent_id[0], 'Moderate', None, 1, 1),
                                Inst_param_value(10, 3, inst_parent_id[0], 'Substantial', None, 1, 1),
                                Inst_param_value(11, 2, inst_parent_id[0], 'minor', None, 1, 1),
                                Inst_param_value(12, 4, inst_parent_id[0], 'Lower division', None, 1, 1),
                                Inst_param_value(13, 4, inst_parent_id[0], 'Upper division', None, 1, 1),
                                Inst_param_value(14, 4, inst_parent_id[0], 'Graduate', None, 1, 1),
                                ]
            session.add_all(inst_param_value)
            session.commit()
            logger.info("inst_param_value data inserted.")
    except Exception as e:
        session.rollback()
        logger.info("error in inserting Inst_param_value")
        pass

def insert_into_area(area_title, inst_id):
    logger.info("inserting into Area table")
    try:
        if not table_exists(engine, 'area'):
            Base.metadata.tables['area'].create(engine)
            logger.info("table created")
        logger.debug("current area title: %s" % area_title)
        uniq_id = str(uuid.uuid4())
        external_id = hashlib.md5(area_title.encode('utf-8')).hexdigest()
        count = session.query(Area.external_id).where(Area.name == area_title).all()
        if len(count) > 0:
            logger.info("Duplicate record found")
        else:
            area_table = Area(uniq_id, external_id, area_title, inst_id[0], datetime.now(), created_by[0],
                              datetime.now(),
                              updated_by[0])
            session.add(area_table)  # persists data
            session.commit()  # commit and close session
            logger.info("data inserted into Area table")
    except Exception as e:
        session.rollback()
        logger.debug("Error raised in insert_into_area(): %s" % e)
        pass
    session.close()


def insert_into_degree(degree, inst_id):
    logger.info("inserting into Degree table")
    try:
        if not table_exists(engine, 'degree'):
            Base.metadata.tables['degree'].create(engine)
            logger.info("table created")
            # print("table created in database")

        # degree = convert_list_to_str([degree]).strip()
        uniq_id = str(uuid.uuid4())
        external_id = hashlib.md5(degree.encode('utf-8')).hexdigest()
        count = session.query(Degree.external_id).where(Degree.external_id == external_id).all()
        if len(count) > 0:
            logger.info("Duplicate record found")
        else:
            degree_table = Degree(uniq_id, external_id, degree, inst_id[0], datetime.now(), created_by[0],
                                  datetime.now(), updated_by[0])
            session.add(degree_table)  # persists data
            session.commit()  # commit and close session
            logger.info("data inserted into Degree table")
    except Exception as e:
        session.rollback()
        logger.debug("Error raised in degree table: %s" % e)
        pass
    session.close()


def insert_into_degree_level(degree, inst_param_group_level, inst_param_value_level):
    logger.info("inserting into Degree_level table")
    global degree_id, level_id
    try:
        if not table_exists(engine, 'degree_level'):
            Base.metadata.tables['degree_level'].create(engine)
            logger.info("table created")
        # degree = convert_list_to_str(data['degree']).strip()
        try:
            degree_id = session.query(Degree.id).filter(Degree.name == degree).one()
            sub_query = session.query(Inst_param_group.id).where(Inst_param_group.name == inst_param_group_level,
                                                                 Inst_param_value.name.ilike(inst_param_value_level))
            level_id = session.query(Inst_param_value.id).where(
                Inst_param_value.inst_param_group_id.in_(sub_query)).all()
        except Exception as e:
            session.rollback()
            logger.debug("No id found in degree_level: %s" % e)
            pass
        try:
            count = session.query(Degree_level.id).where(
                Degree_level.degree_id == degree_id[0] and Degree_level.level_id == level_id[0][0]).all()
            if len(count) > 0:
                print("duplicate key found")
            else:
                degree_level_table = Degree_level(degree_id[0], level_id[0][0])
                session.add(degree_level_table)  # persists data
                session.commit()  # commit and close session
                logger.info("data inserted into Degree_level table")
                print("degree-level data Inserted")
                session.close()
        except Exception as e:
            print("error while inserting data into degree-level ", e)
            pass
    except Exception as e:
        session.rollback()
        logger.debug("Error raised in insert_into_degree_level(): %s" % e)
        pass


def insert_into_program(program_url, program_name, program_degree, program_description, program_level, study_type, unique_id, inst_parent_id):
    global get_prog_level_id, degree_id
    print("inserting into program table")
    try:
        if not table_exists(engine, 'program'):
            Base.metadata.tables['program'].create(engine)
            logger.info("table created")
        try:
            prog_level_id = select(Inst_param_value.id).where(Inst_param_value.inst_param_group_id.in_(
                select(Inst_param_group.id).where(Inst_param_group.name == prog_level,
                                                  Inst_param_value.name.ilike(prog_type))))
            get_id = conn.execute(prog_level_id).fetchall()
            get_prog_level_id = get_tuple_id(get_id)
            degree_id = session.query(Degree.id).filter(Degree.name == program_degree).one()
            session.commit()
        except Exception as e:
            session.rollback()
            pass
        try:
            uniq_id = str(uuid.uuid4())
            external_id = hashlib.md5(program_url.encode('utf-8')).hexdigest()
            count = session.query(Program.external_id).where(Program.external_id == external_id).all()
            if len(count) > 0:
                logger.info("Duplicate record found")
            else:
                program_table = Program(uniq_id, external_id, get_prog_level_id[0], degree_id[0], inst_parent_id[0],
                                        unique_id[0], program_name, program_description,None, None, None, None,
                                        program_url, None, None, None, None, datetime.now(), created_by[0],
                                        datetime.now(), updated_by[0])
                session.add(program_table)
                session.commit()
                logger.info("data inserted into program table")
                session.close()
        except Exception as e:
            logger.debug("Error raised while inserting into program: %s" % e)
    except Exception as e:
        session.rollback()


def insert_into_program_area(program_url, prog_area_name):
    logger.info("inserting into program_area table")
    global program_id, prog_area
    try:
        if not table_exists(engine, 'program_area'):
            Base.metadata.tables['program_area'].create(engine)
            logger.info("table created")
            # print("table created in database")
        try:
            program_id = session.query(Program.id).filter(Program.external_link == program_url).one()
            prog_area = session.query(Area.id).where(Area.name == prog_area_name).one()
        except Exception as e:
            session.rollback()
            pass

        program_area_table = Program_area(program_id[0], prog_area[0])
        session.add(program_area_table)  # persists data
        session.commit()  # commit and close session
        logger.info("data inserted into program_area table")
        # print("program area data Inserted")
        session.close()
    except Exception as e:
        session.rollback()
        logger.debug("Duplicate data found in program_area")
        # print("Duplicate data found in program_area")
        pass
    return program_id


def insert_into_program_college(program_id, college_name):
    print("Inserting into program-college table")
    try:
        if not table_exists(engine, 'program_college'):
            Base.metadata.tables['program_college'].create(engine)
            logger.info("table created")
        try:
            prog_college_id = session.query(Institution.id).where(Institution.name == college_name).first()
            program_college_table = Program_college(program_id[0], prog_college_id[0])
            session.add(program_college_table)  # persists data
            session.commit()  # commit and close session
            logger.info("data inserted into program-college table")
            session.close()
            session.commit()
        except Exception as e:
            session.rollback()
            logger.debug("duplicate data found in program-college(): ")
            pass

    except Exception as e:
        session.rollback()
        logger.debug("error found in program-college() %s" % e)
        # print("duplicate found in program_location: ", e)
        pass


def Insert_into_graduate_admission_req(program_id, admission_description):
    if not table_exists(engine, 'admission_req'):
        Base.metadata.tables['admission_req'].create(engine)
        logger.info("table created")
    try:
        uniq_id = str(uuid.uuid4())
        external_id = hashlib.md5(str(str(program_id[0]) + admission_description).encode('utf-8')).hexdigest()
        count = session.query(Admission_req.external_id).where(Admission_req.external_id == external_id).all()
        if len(count) > 0:
            logger.info("Duplicate record found")
        else:
            try:
                Admission_req_table = Admission_req(uniq_id, external_id, program_id[0], admission_description,
                                                    datetime.now(), created_by[0], datetime.now(), updated_by[0])
                session.add(Admission_req_table)
                session.commit()
                logger.info("data inserted into program table")
                session.close()
            except Exception as e:
                print("error raised in admission-req table while inserting :", e)
                session.rollback()
    except Exception as e:
        print("error raised in admission-req table :", e)


def insert_into_requirement_group(program_id, program_url, program_name, academic_year, total_credits, code):
    print("inserting into requirement_group table")
    logger.info("inserting into requirement_group table")
    try:
        if not table_exists(engine, 'rqmt_group'):
            Base.metadata.tables['rqmt_group'].create(engine)
            logger.info("table created in database")
        get_academic_year = academic_year.split("-")
        start_year = int(get_academic_year[0])
        end_year = int(get_academic_year[1])
        uniq_id = str(uuid.uuid4())
        external_id = hashlib.md5(program_url.encode('utf-8')).hexdigest()
        count = session.query(Requirement_group.external_id).where(Requirement_group.external_id == external_id).all()
        if len(count) > 0:
            logger.info("Duplicate record found")
        else:
            requirement_group_table = Requirement_group(uniq_id, external_id, program_id[0], program_name.strip(), code,
                                                        None, 'Ects', total_credits, None,None, None, None,
                                                        None, None,None, None, None,None, None,None, program_url,
                                                        academic_year, start_year, end_year,
                                                        datetime.now(), created_by[0], datetime.now(), updated_by[0])
            session.add(requirement_group_table)
            session.commit()
            logger.info("data inserted into requirement_group")
            session.close()

    except Exception as e:
        session.rollback()
        logger.debug("Error raised in Requirement_group: %s" % e)
        # print("Error raised in Requirement_group:", e)
        pass


def insert_into_requrement_category(inst_id, course_category):
    print("calling & inserting requrement_category-table()")
    try:
        uniq_id = str(uuid.uuid4())
        category_external_id = hashlib.md5(str(course_category).encode('utf-8')).hexdigest()
        count = session.query(Graduate_req_category.external_id).where(Graduate_req_category.name == course_category).all()
        if len(count) > 0:
            logger.info("Duplicate record found")
        else:
            Graduate_deg_table = Graduate_req_category(uniq_id, category_external_id, inst_id[0], course_category,
                                                       datetime.now(), created_by[0], datetime.now(), updated_by[0])
            session.add(Graduate_deg_table)
            session.commit()
            logger.info("data inserted into Graduate_requirement_group table")
            session.close()
    except Exception as e:
        session.rollback()
        logger.debug("Error raised in Requirement_category: %s" % e)
        # print("Error raised in Requirement_group:", e)
        pass


def insert_into_term(req_group_id, program_url, term_head):
    print("calling term table")
    try:
        if not table_exists(engine, 'term'):
            Base.metadata.tables['term'].create(engine)
            logger.info("table created")
        uniq_id = str(uuid.uuid4())
        external_id = hashlib.md5(str(str(req_group_id[0]) + term_head).encode('utf-8')).hexdigest()
        count = session.query(Term.external_id).where(Term.external_id == external_id).all()
        if len(count) > 0:
            logger.info("Duplicate record found")
        else:
            term_table = Term(uniq_id, external_id, req_group_id[0], term_head, None, None, None, None,None, None, None,
                               None, datetime.now(), created_by[0], datetime.now(), updated_by[0])
            session.add(term_table)
            session.commit()
            logger.info("data inserted into term table")
            session.close()

    except Exception as e:
        session.rollback()
        logger.debug("Error in insert_into_term(), %s" % e)
        pass


def insert_into_rqmt_group_rqmt_category(req_group_id, inst_parent_id, course_category):
    global req_category_id
    try:
        req_category_id = session.query(Graduate_req_category.id).where(Graduate_req_category.name == course_category).first()
        count = session.query(Rqmt_group_rqmt_category.id).where(Rqmt_group_rqmt_category.rqmt_group_id==req_group_id[0] and Rqmt_group_rqmt_category.rqmt_category_id==req_category_id[0]).all()
        if len(count)>0:
            print("duplicate exists with keys")
        else:
            Rqmt_grp_rqmt_category_table = Rqmt_group_rqmt_category(req_group_id[0], req_category_id[0], None, None, None)
            session.add(Rqmt_grp_rqmt_category_table)
            session.commit()
            logger.info("data inserted into program table")
            session.close()
    except Exception as e:
        session.rollback()
        print("Error raised as Requirement_group_Requirement_category-table as:", e)
    return req_category_id


def insert_into_requirement(program_url,course_code, requirement_group_id, each_requirement, max_credits, rqmt_group_rqmt_category_id):
    print("calling requirement_table")
    try:
        if not table_exists(engine, 'requirement'):
            Base.metadata.tables['requirement'].create(engine)
            logger.info("table created")
        uniq_id = str(uuid.uuid4())
        external_id = hashlib.md5(str(program_url+each_requirement+ str(max_credits)).encode('utf-8')).hexdigest()
        count = session.query(Requirement.external_id).where(Requirement.external_id == external_id).all()
        if len(count) > 0:
            # print("Duplicate record found")
            logger.info("Duplicate record found")
        else:
            requirement_table = Requirement(uniq_id, external_id, requirement_group_id[0], rqmt_group_rqmt_category_id[0], each_requirement, None,
                                            'Ects', None, max_credits, None, None, None, datetime.now(), created_by[0],
                                             datetime.now(),updated_by[0])
            session.add(requirement_table)
            session.commit()
            logger.info("data inserted into requirement table")
            session.close()

    except Exception as e:
        session.rollback()
        logger.debug("Error for insert_into_requirement(): %s" % e)
        pass


def insert_into_course_table(inst_id, course_code, course_code_link, course_name, course_description, course_hours):
    global course_level_id
    print("calling course table")
    if not table_exists(engine, 'course'):
        Base.metadata.tables['course'].create(engine)
        logger.info("table created")
    uniq_id = str(uuid.uuid4())
    external_id = hashlib.md5(course_code.encode('utf-8')).hexdigest()
    count = session.query(Course.external_id).where(Course.external_id == external_id).all()
    try:
        get_course_code = re.findall(r'\S+', course_code)
        code_prefix = get_course_code[0].strip()
        code_suffix = get_course_code[1].strip()
        try:
            if int(code_suffix) in range(100, 299):
                print("number found in range (100-299) as Lower division:", code_suffix)
                course_level_id = session.query(Inst_param_value.id).filter(
                    Inst_param_value.name == 'Lower division').first()
            if int(code_suffix) in range(300, 499):
                print("number found in range (300-499) as Upper division:", code_suffix)
                course_level_id = session.query(Inst_param_value.id).filter(
                    Inst_param_value.name == 'Upper division').first()
            if int(code_suffix) in range(500, 10000):
                print("number found in range (above 500) as Graduate:", code_suffix)
                course_level_id = session.query(Inst_param_value.id).filter(Inst_param_value.name == 'Graduate').first()
        except Exception as e:
            print("error raised while getting course-level-id as :", e)
            course_level_id = None
        if course_hours is not None:
            credit = 1
        else:
            credit = None
        if len(count) > 0:
            # print("Duplicate record found")
            logger.info("Duplicate record found")
        else:
            course_table = Course(uniq_id, external_id, inst_id[0], course_name, course_code, code_prefix, code_suffix, None,
                                  course_description, credit, "Ects", None, int(course_hours), course_code_link,
                                  None, None, course_level_id[0], datetime.now(), created_by[0], datetime.now(), updated_by[0])
            session.add(course_table)  # persists data
            session.commit()  # commit and close session
            logger.info("data inserted into course table")
            session.close()
            # print("course data Inserted")
    except Exception as e:
        session.rollback()
        logger.debug("Error raised while inserting into insert_into_course(): %s" % e)
        print("Error raised while inserting into insert_into_course(): %s", e)
        pass


def insert_into_requirement_variable(inst_parent_id, course_code, requirement, requirement_id, data):
    global value_id
    print("calling requirement-variable table")
    logger.info("insert into requirement-variable table")
    if not table_exists(engine, 'rqmt_variable'):
        Base.metadata.tables['rqmt_variable'].create(engine)
        logger.info("table created")
    # requirement_id = session.query(Requirement.id).where(Requirement.external_id == req_external_id).one()
    uniq_id = str(uuid.uuid4())
    external_id = hashlib.md5(str(course_code+requirement).encode('utf-8')).hexdigest()
    try:
        entity = 'course'
        # course_id from Course
        try:
            value_id = session.query(Course.id).where(Course.code == data['course_code'][0]).first()
            course_id = value_id[0]
        except Exception as e:
            # pass
            course_id = None
            entity = "elective"
            logger.debug("no id found for getting (value_id) in-course: %s" % e)
            pass
            # print("no id found in (value_id)-course: ", e)
        post_data_into_rqmt_variable(uniq_id, external_id, requirement_id[0], requirement, entity, course_id)
    except Exception as e:
        logger.debug("error raised entity :course: %s" % e)


def post_data_into_rqmt_variable(uniq_id, external_id, requirement_id, subject, entity, value_id):
    logger.info("inserting data-into post_data_into_rqmt_variable()")
    try:
        count = session.query(Requirement_variable.external_id).where(
            Requirement_variable.external_id == external_id).all()
        if len(count) > 0:
            logger.info("Duplicate record found")
            # print("Duplicate record found")
        else:
            requirement_variable_table = Requirement_variable(uniq_id, external_id, requirement_id, subject, entity,
                                                              value_id, datetime.now(), created_by[0], datetime.now(),
                                                              updated_by[0])
            session.add(requirement_variable_table)  # persists data
            session.commit()  # commit and close session
            logger.info("data inserted into requirement_variable table")
            # print("requirement_variable data Inserted", "\n")
            session.close()
    except Exception as e:
        session.rollback()
        logger.error("Error raised in post_data_into_rqmt_variable as: %s" % e)
        # print("Error in post_data_into_rqmt_variable(): ", e)
        pass


def collect_all_program_page(program_url, inst_param_group_level, inst_param_value_level, program_level, prog_type):
    global inst_parent_id, current_program_id
    soup = prepare_soup(program_url)
    collect_program_index_links = soup.find('div', {'class': 'form-inline text-left'})

    collect_department_link = collect_program_index_links.findAll('li')[1].a['href']
    collect_department_soup = prepare_soup(collect_department_link)
    find_all_tags = collect_department_soup.find('div', {'class': 'panel-body'})
    if yaml_obj.get(Website_URL).get('DEGREE_TYPE') == "Masters":
        print("this is masters program")
        try: # getting institution parent-id
            university_name = yaml_obj.get(Website_URL).get('UNIVERSITY')
            inst_parent_id = session.query(Institution.id).filter_by(name=university_name).one()
        except Exception as e:
            logger.debug("Exception raised:No id found in insert_colleges_into_institution(): %s" % e)
            pass

        get_all_subject_links= find_all_tags.findAll('div', {'style':'color: #1b96d0; margin-left: 20px; padding: 5px'})
        for each_subject_links in get_all_subject_links:
            collect_sub_links = each_subject_links.findAll('a')  # collect each Department (program|Curriculum)
            print("current masters program is: ",collect_sub_links[0].text)
            try:
                master_program_name = collect_sub_links[0].text
                current_program_url = collect_sub_links[0]['href']
                program_page_soup = prepare_soup(current_program_url)  # scrape each program page
                current_program_id = scrape_program_page(inst_parent_id, master_program_name, current_program_url, program_page_soup,
                                             inst_param_group_level, inst_param_value_level, program_level, prog_type)
            except Exception as e:
                print("error raised while calling ,,,master,,, scrape program page as: ", e)
            try:
                program_curriculum_url = collect_sub_links[1]['href']
                program_curriculum_soup = prepare_soup(program_curriculum_url)
                # current_program_id = (5,)
                scrape_program_curriculum_page(inst_parent_id, current_program_id, program_curriculum_soup,
                                               program_curriculum_url)  # scrape each program curriculum & requirement-page
            except Exception as e:
                print("error raised while calling ,,,master,,, scrape program curriculum page as: ", e)
    else:
        print("this is undergraduate program")
        get_all_labels = find_all_tags.findAll('label')
        try: # getting institution parent-id
            university_name = yaml_obj.get(Website_URL).get('UNIVERSITY')
            inst_parent_id = session.query(Institution.id).filter_by(name=university_name).one()
        except Exception as e:
            logger.debug("Exception raised:No id found in insert_colleges_into_institution(): %s" % e)
            pass
        for each_label in get_all_labels:
            get_label_link = each_label.a['href']
            print("current_program scraping is :", each_label.text)
            collect_label_soup = prepare_soup(get_label_link)
            collect_label_index = collect_label_soup.find('div', {'class': 'form-inline text-left'})
            get_department_link = collect_label_index.findAll('li')[1].a['href']
            get_department_soup = prepare_soup(get_department_link)
            find_sub_links = get_department_soup.find('div', {'class': 'panel-body'})
            collect_sub_links = find_sub_links.findAll('a')  # collect each Department (program|Curriculum)
            try:
                current_program_url = collect_sub_links[0]['href']
                graduate_program_name = collect_sub_links[0].text
                program_page_soup = prepare_soup(current_program_url)  # scrape each program page
                current_program_id = scrape_program_page(inst_parent_id, graduate_program_name, current_program_url, program_page_soup, inst_param_group_level, inst_param_value_level, program_level, prog_type)
            except Exception as e:
                print("error raised while calling scrape program page as: ", e)
            try:
                program_curriculum_url = collect_sub_links[1]['href']
                program_curriculum_soup = prepare_soup(program_curriculum_url)
                # current_program_id = (5,)
                scrape_program_curriculum_page(inst_parent_id, current_program_id, program_curriculum_soup,
                                               program_curriculum_url)  # scrape each program curriculum & requirement-page
            except Exception as e:
                print("error raised while calling scrape program curriculum page as: ", e)


def scrape_program_page(inst_parent_id, master_program_name, program_url, program_page_soup, inst_param_group_level, inst_param_value_level, program_level, prog_type):
    global university_name
    get_program_page_soup = program_page_soup.find('div', {'class': 'form-inline text-left'})
    collect_program_sublinks = get_program_page_soup.findAll('li')

    program_description = prepare_soup(collect_program_sublinks[1].a['href'])
    get_program_description = program_description.find('div', {'class': 'panel-body'})
    collect_program_description = html_text.extract_text(f"{get_program_description}")

    prog_name_degree = prepare_soup(collect_program_sublinks[3].a['href'])
    get_prog_name_degree = prog_name_degree.find('div', {'class': 'panel-body'})
    collect_get_prog_name_degree = html_text.extract_text(f"{get_prog_name_degree}")
    if yaml_obj.get(Website_URL).get('DEGREE_TYPE') == "Masters":
        program_name = master_program_name
    else:
        program_name = collect_get_prog_name_degree.split(",")[0]
    program_degree = collect_get_prog_name_degree.split(",")[1].split(" ")[1].split("'")[0]

    # Length of Program and Number of Credits

    Admission_requirements = prepare_soup(collect_program_sublinks[6].a['href'])
    get_admission_req = Admission_requirements.find('div', {'class': 'panel-body'})
    collect_get_admission_req = html_text.extract_text(f"{get_admission_req}")

    # Qualification and Graduation Requirements and Regulations

    study_type = prepare_soup(collect_program_sublinks[18].a['href'])  # Mode of Study(Online/ofline/fulltime)
    get_study_type = study_type.find('div', {'class': 'panel-body'})
    collect_study_type = html_text.extract_text(f"{get_study_type}")

    get_program_unique_id = prepare_soup(collect_program_sublinks[16].a['href'])  # program_unique_number/id
    get_unique_id = get_program_unique_id.find('h3', {'class': 'panel-title font-bold'})
    program_unique_id = html_text.extract_text(f"{get_unique_id}")
    unique_id = re.findall(r'\d+', program_unique_id)
    # ****** -------------------------------------------------------------------- ******
    print("calling area table")
    insert_into_area(program_name, inst_parent_id)

    print("calling degree table")
    insert_into_degree(program_degree, inst_parent_id)

    print("calling degree_level tabel")
    insert_into_degree_level(program_degree, inst_param_group_level, inst_param_value_level)

    print(" calling program table")
    insert_into_program(program_url, program_name, program_degree, collect_program_description, program_level, collect_study_type, unique_id, inst_parent_id)

    print(" calling program_area table")
    program_id = insert_into_program_area(program_url, program_name)

    print(" calling program_college table")
    insert_into_program_college(program_id, university_name)

    print("calling addmission req table")
    Insert_into_graduate_admission_req(program_id, collect_get_admission_req)

    return program_id


def scrape_program_curriculum_page(inst_parent_id, program_id, soup, program_url):
    global term, requirement_id
    try:
        term = "Semester 1"
        get_academic_year = soup.findAll('div', {'class': 'container'})[3].h4.text
        # requrement - group --------------------------------------------------------table
        academic_year = get_academic_year.split("|")[0].strip()
        program_name = get_academic_year.split("|")[1].strip()
        data = extract_data_using_selector_lib(soup, "Get_course_Requirement", Website_URL)
        # total_credits = re.findall(r'\d+', data['total_credits'])[0]
        total_credits = re.findall(r'\d+',soup.find('div',{'style':'float:right'}).text)[0]
        get_unique_code = re.findall(r'\d+',soup.find('div',{'class':'panel-heading'}).text)[0]
        insert_into_requirement_group(program_id, program_url, program_name, academic_year, total_credits, get_unique_code)
        req_group_id = session.query(Requirement_group.id).where(Requirement_group.external_link == program_url).first()
        # reuirement ----------------------------------------------------------------table
        get_all_table = soup.find('div', {'class': 'panel-body'})
        # collect_each_label_for_table = get_all_table.findAll('label')
        collect_all_tables = get_all_table.findAll("table")
        for each_table in collect_all_tables:           # original code
            get_table_body = each_table.find('tbody')
            collect_tr = get_table_body.findAll('tr')
            try:
                for each_td in collect_tr:

                    data = extract_data_using_selector_lib(each_td, "Get_course_Requirement", Website_URL)
                    if data['course_code'] is not None:
                        if data['course_hours'] and data['course_ects'] is not None:
                            for course_code, each_requirement, max_credits, course_category in zip(data['course_code'], data['course_name'],
                                      data['course_ects'], data['course_elective']):
                                # data['course_name_link']
                                print("Requirement name :", each_requirement, "", "max_credits: ", max_credits)
                                # 1. requirement_category table  (course_category)
                                insert_into_requrement_category(inst_parent_id, course_category)
                                try:
                                    term = "Semester 1"
                                    insert_into_term(req_group_id, program_url, term)
                                except Exception as e:
                                    print("error raised while inserting-into-term as:", e)

                                # 1.1 requirement_group_requirement_category table
                                req_category_id = insert_into_rqmt_group_rqmt_category(req_group_id, inst_parent_id, course_category)
                                rqmt_group_rqmt_category_id = session.query(Rqmt_group_rqmt_category.id).where(Rqmt_group_rqmt_category.rqmt_group_id==req_group_id[0] and Rqmt_group_rqmt_category.rqmt_category_id == req_category_id[0]).first()

                                # 2. requirement table
                                try:
                                    insert_into_requirement(program_url, course_code, req_group_id, each_requirement, max_credits, rqmt_group_rqmt_category_id)
                                except Exception as e:
                                    print("error raised while inserting into requirement table ", e)

                                # 3. requirement-term mapping

                                try:
                                    print("calling req-term table")
                                    req_external_id = hashlib.md5(str(program_url+each_requirement + str(max_credits)).encode('utf-8')).hexdigest()
                                    requirement_id = session.query(Requirement.id).where(Requirement.external_id == req_external_id).first()
                                    term_external_id = hashlib.md5(str(str(req_group_id[0]) + term).encode('utf-8')).hexdigest()
                                    term_id = session.query(Term.id).where(Term.external_id == term_external_id).first()
                                    requirement_term_table = Requirement_term(requirement_id[0], term_id[0])
                                    session.add(requirement_term_table)  # persists data
                                    session.commit()  # commit and close session
                                    logger.info("data inserted into requirement_term ")
                                    print("data inserted into requirement_term ")
                                    session.close()
                                except Exception as e:
                                    session.rollback()
                                    print("error raised while inserting into req_term table ", e)
                                # Course table
                                try:
                                    scrape_course_page(inst_parent_id, data, None)
                                except Exception as e:
                                    print("error raised while calling into scrape_course_page() ", e)

                                # requirement_variable table
                                try:
                                    insert_into_requirement_variable(inst_parent_id, course_code, each_requirement, requirement_id, data)
                                except Exception as e:
                                    print("error raised while calling into scrape_course_page() ", e)
                    else:
                        print("getting electives")
                        course_name_link = each_td.a['href']
                        for course_name, course_hours, course_category in zip(data['course_name'],data['course_ects'], data['course_elective']):
                            insert_into_requrement_category(inst_parent_id, course_category)

                            # 1. requirement_group_requirement_category table
                            req_category_id = insert_into_rqmt_group_rqmt_category(req_group_id, inst_parent_id,
                                                                                   course_category)
                            rqmt_group_rqmt_category_id = session.query(Rqmt_group_rqmt_category.id).where(
                                Rqmt_group_rqmt_category.rqmt_group_id == req_group_id[
                                    0] and Rqmt_group_rqmt_category.rqmt_category_id == req_category_id[0]).first()
                            try:
                                insert_into_requirement(program_url, course_name_link, req_group_id, course_name, course_hours, rqmt_group_rqmt_category_id)
                            except Exception as e:
                                print("error raised while inserting into requirement table ", e)

                            try:
                                req_external_id = hashlib.md5(
                                    str(program_url + course_name).encode('utf-8')).hexdigest()
                                requirement_id = session.query(Requirement.id).where(
                                    Requirement.external_id == req_external_id).first()
                                term_external_id = hashlib.md5(str(str(req_group_id[0]) + term).encode('utf-8')).hexdigest()
                                term_id = session.query(Term.id).where(Term.external_id == term_external_id).first()
                                requirement_term_table = Requirement_term(requirement_id[0], term_id[0])
                                session.add(requirement_term_table)  # persists data
                                session.commit()  # commit and close session
                                logger.info("data inserted into requirement_term ")
                                session.close()
                            except Exception as e:
                                session.rollback()
                                print("error raised while inserting into req_term table ", e)

                            # Course table
                            try:
                                scrape_course_page(inst_parent_id, data, course_name_link)
                                print("inserting into course table completed")
                            except Exception as e:
                                print("error raised while calling into scrape_course_page() ", e)

                            # requirement_variable table
                            try:
                                insert_into_requirement_variable(inst_parent_id, "None", course_name, requirement_id, data)
                            except Exception as e:
                                print("error raised while calling into scrape_course_page() ", e)

            except Exception as e:
                print("error raised while collecting table-data", e)
    except Exception as e:
        print("error raised while calling scrape_curricukum page", e)


def scrape_course_page(inst_id, data, course_name_link):
    global get_course_soup
    if data['course_code'] is not None:
        for course_code, course_code_link, course_name, course_hours in zip(data['course_code'], data['course_code_link'],data['course_name'],
                                                           data['course_ects']):
            get_course_soup = prepare_soup(course_code_link)
            course_data = extract_data_using_selector_lib(get_course_soup, "Get_course_page", Website_URL)
            insert_into_course_table(inst_id, course_code, course_code_link, course_name, course_data['course_description'], course_hours)
    else:
        if data['course_name_link'] is not "":
            if course_name_link not in check_course_pagination_links:
                check_course_pagination_links.append(course_name_link)
                print("course -pagination started here")
                print("pagination-link :", course_name_link)
                get_course_page_soup = prepare_soup(course_name_link)
                data = extract_data_using_selector_lib(get_course_page_soup, "Get_course_pagination", Website_URL)
                print("total course collected on page-1 :", len(data['course_codes_multiple']))
                for course_code, course_code_link, course_name, course_hours in zip(data['course_codes_multiple'],
                                           data['course_codes_links'], data['course_name'], data['course_ects']):
                    get_course_soup = prepare_soup(course_code_link)
                    course_data = extract_data_using_selector_lib(get_course_soup, "Get_course_page", Website_URL)
                    insert_into_course_table(inst_id, course_code, course_code_link, course_name,
                                             course_data['course_description'], course_hours)
                    print("calling course rable for pagination")
                print("pagination completed for", data['course_name'][0], " ", " pagination -1")
                try:
                    if yaml_obj.get(Website_URL).get('Pagination').get('required'):
                        page_numbers = extract_data_using_selector_lib(get_course_page_soup, "Collect_Pagination_numbers", Website_URL)
                        print("pages found: %s", page_numbers['total_pages_collected'])
                        count = 1
                        pagination_data = extract_data_using_selector_lib(get_course_page_soup, "Collect_Pagination_urls", Website_URL)
                        for each_pagination_url in pagination_data['total_pages_urls_collected']:
                            if count < (int(len(page_numbers['total_pages_collected'])) - 2):
                                time.sleep(2)
                                get_page_soup = prepare_soup(each_pagination_url)
                                data = extract_data_using_selector_lib(get_page_soup, "Get_course_pagination", Website_URL)

                                try:
                                    count += 1
                                    print("next page number: %s", count)
                                    print("total course collected on page-", count, " is ",len(data['course_codes_multiple']))
                                    print("page -urls :", each_pagination_url, "\n")
                                    for course_code, course_code_link, course_name, course_hours in zip(data['course_codes_multiple'],
                                            data['course_codes_links'], data['course_name'], data['course_ects']):
                                        get_course_soup = prepare_soup(course_code_link)
                                        course_data = extract_data_using_selector_lib(get_course_soup, "Get_course_page",Website_URL)
                                        insert_into_course_table(inst_id, course_code, course_code_link, course_name,
                                                                 course_data['course_description'], course_hours)
                                    print("running pagination completed ...!")

                                except Exception as e:
                                    logger.debug("Getting Error while collecting next-page data:  %s" % e)
                                    pass
                            else:
                                print("Pagination completed..!")
                except Exception as e:
                    logger.debug("Getting Error while entering to collecting next-page data:  %s" % e)
                    pass
            else:
                print("this course-pagination is already scraped :", course_name_link)


if __name__ == '__main__':
    logger.info("work site: Istnbul Bilgi University")
    global collect_all_degree_urls, Website_URL, master_Website_URL
    Bilgi_Website_URL = [
        "https://ects-bilgi-edu-tr.translate.goog/Institutional?_x_tr_sl=tr&_x_tr_tl=en&_x_tr_hl=en-GB&_x_tr_pto=sc",
    ]
    try:
        for Bigli_Website_URL in Bilgi_Website_URL:
            # logger.debug("scraping website: %s" % Website_URL)
            print("Bigli scraping website-started :", Bigli_Website_URL)
            soup = prepare_soup(Bigli_Website_URL)

            collect_index_links = soup.find('div', {'class': 'form-inline text-left'})
            get_program_link = collect_index_links.findAll('li')[7].a['href']
            print(get_program_link)
            get_soup = prepare_soup(get_program_link)
            try:
                collect_all_degree_urls = get_soup.find('div', {'class': 'col-md-3 printer-hide'}).findAll('li')
                Website_URL = collect_all_degree_urls[2].a['href']   # Graduate programs starts here
            except Exception as e:
                print("failed to get the graduate url ,:", e)
            university_name = yaml_obj.get(Website_URL).get('UNIVERSITY')
            inst_param_group_level = yaml_obj.get(Website_URL).get('INST_PARAM_GROUP_LEVEL')
            inst_param_value_level = yaml_obj.get(Website_URL).get('INST_PARAM_VALUE_LEVEL')
            prog_level = yaml_obj.get(Website_URL).get('PROGRAM_LEVEL')  # 'PROGRAM_LEVEL'
            prog_type = yaml_obj.get(Website_URL).get('PROGRAM_TYPE')  # '%Undergraduate%'
            # inserting_into institution & inst_param_values
            print("inserting into Institution table")
            insert_into_university_institution(university_name)
            print("inserting into Inst_param_value")
            master_data_into_inst_param_values(university_name)

            try:
                get_soup = prepare_soup(Website_URL) # all Bachelors department-links collected
                get_all_programs = get_soup.findAll('div', {'class': 'panel panel-default'})
                for each_program in get_all_programs:
                    # testing single program(first-program)
                    # testing_program_url = get_all_programs[0].a['href']
                    get_each_program_link = each_program.a['href']
                    collect_all_program_page(get_each_program_link, inst_param_group_level, inst_param_value_level,
                                             prog_level, prog_type)
                print("Bilgi university scraping completed.. for All Graduate programs.!")
            except Exception as e:
                print("error raised collecting soup and calling program-page function  for graduate ", e)

            try: # Master program scraping started
                print("Master program scraping started...!")
                Website_URL = collect_all_degree_urls[3].a['href']  # master programs starts here
                university_name = yaml_obj.get(Website_URL).get('UNIVERSITY')
                inst_param_group_level = yaml_obj.get(Website_URL).get('INST_PARAM_GROUP_LEVEL')
                inst_param_value_level = yaml_obj.get(Website_URL).get('INST_PARAM_VALUE_LEVEL')
                prog_level = yaml_obj.get(Website_URL).get('PROGRAM_LEVEL')  # 'PROGRAM_LEVEL'
                prog_type = yaml_obj.get(Website_URL).get('PROGRAM_TYPE')  # '%Undergraduate%'
                try:
                    get_soup = prepare_soup(Website_URL)  # all Masters department-links collected
                    get_all_programs = get_soup.findAll('div', {'class': 'panel panel-default'})
                    for each_program in get_all_programs:
                        get_each_program_link = each_program.a['href']
                        collect_all_program_page(get_each_program_link, inst_param_group_level, inst_param_value_level,
                                                 prog_level, prog_type)
                    print("Bilgi university scraping completed.. for All master programs.!")
                except Exception as e:
                    print("error raised collecting soup and calling  program-page function  for masters ", e)
            except Exception as e:
                print("error raised while collecting master program url ", e)
            print("scraping completed...!")
    except Exception as e:
        print("error raised while starting the scraping", e)
    driver.close()
    driver.quit()
