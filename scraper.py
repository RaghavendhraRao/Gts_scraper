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

# /data/project/
with open(r'logging_config_template.yaml', 'r') as f:
    config = yaml.safe_load(f.read())
    config['handlers']['all']['filename'] = os.path.join(config['handlers']['all']['filename'] + "gts_scrape" + ".log")
    logging.config.dictConfig(config)
logger = logging.getLogger(__name__)

with open(r'selectors.yaml', 'r') as stream:
    try:
        yaml_obj = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        logger.info("Exception raised while opening selectors.yaml file", exc)
        raise

# # # # --> Prepaing Data to Database
# creating a global list to check the expression for pagination
check_subject_pagination = []

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

ext = Extractor.from_yaml_file('selectors.yaml')
CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))
os.chdir(CURRENT_PATH)
os.chdir('../..')


def extract_data_using_selector_lib(new_soup, typo, Website_URL):
    a = ext.__dict__
    b = a['config'][Website_URL][typo]
    c = Extractor(b)
    data = c.extract(str(new_soup))
    return data


def convert_list_to_str(lst):
    return " ".join(lst)


def isfloat(num):
    try:
        a = float(num)
        return a
    except ValueError:
        return False


def prepare_soup(Website_URL):
    driver.get(Website_URL)
    time.sleep(5)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    return soup


def get_tuple_id(id):
    for i in id:
        return i


def get_boolean(id):
    if id == 'Yes':
        return True
    else:
        return False


def find_math_intensity(a):
    math_intensity_list = ['General', 'Moderate', 'Substantial']
    for i in math_intensity_list:
        if i == a:
            m_intensity = session.query(Inst_param_value.id).filter(Inst_param_value.name == a).first()
            return m_intensity[0]


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
                                Inst_param_value(12, 4, inst_parent_id[0], 'Lower division', None, 1,1),
                                Inst_param_value(13, 4, inst_parent_id[0], 'Upper division', None, 1, 1),
                                Inst_param_value(14, 4, inst_parent_id[0], 'Graduate', None, 1, 1),

                                ##(1021,4,1,'Lower division',NULL,NULL,1), (1022,4,1,'Upper division',NULL,NULL,1),
                                # (1023,4,1,'Graduate',NULL,NULL,1)
                                ]
            session.add_all(inst_param_value)
            session.commit()
            logger.info("inst_param_value data inserted.")
    except Exception as e:
        session.rollback()
        logger.info("error in inserting Inst_param_value")
        pass


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
            institution_table = Institution(uniq_id, external_id, university_name, 'ASU', None, 'University', None,
                                            datetime.now(), created_by[0], datetime.now(), updated_by[0])
            session.add(institution_table)  # persists data
            session.commit()  # commit and close session
            logger.info("Parent-institution data inserted")
    except Exception as e:
        session.rollback()
        logger.debug("Exception raised insert_into_institution-parent() : %s" % e)
        pass
    session.close()


def insert_into_college_institution(data, university_name):  # inserting college/school colleges into institution
    logger.info("inserting child data into Inserting table ")
    global inst_parent_id
    try:
        try:
            institution_name = convert_list_to_str(data['college'])
        except Exception as e:
            institution_name = convert_list_to_str(data)
        try:
            inst_parent_id = session.query(Institution.id).filter_by(name=university_name).one()
        except Exception as e:
            logger.debug("Exception raised:No id found in insert_colleges_into_institution(): %s" % e)
            pass
        uniq_id = str(uuid.uuid4())
        external_id = hashlib.md5(institution_name.encode('utf-8')).hexdigest()
        count = session.query(Institution.external_id).where(Institution.external_id == external_id).all()
        if len(count) > 0:
            logger.info("Duplicate record found")
        else:
            institution_table = Institution(uniq_id, external_id, institution_name, None, None, 'College',
                                            inst_parent_id[0],
                                            datetime.now(), created_by[0], datetime.now(), updated_by[0])
            session.add(institution_table)  # persists data
            session.commit()  # commit and close session
            logger.info("data inserted into Institution table")
    except Exception as e:
        session.rollback()
        logger.debug("Exception raised: in insert_colleges_into_institution(): %s" % e)
        pass
    session.close()
    return inst_parent_id


def insert_into_area(area_title, inst_id):
    logger.info("inserting into Area table")
    try:
        if not table_exists(engine, 'area'):
            Base.metadata.tables['area'].create(engine)
            logger.info("table created")
        logger.debug("current area title: %s" % area_title)
        uniq_id = str(uuid.uuid4())
        external_id = hashlib.md5(area_title.encode('utf-8')).hexdigest()
        count = session.query(Area.external_id).where(Area.external_id == external_id).all()
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


def insert_into_degree(data, inst_id):
    logger.info("inserting into Degree table")
    try:
        if not table_exists(engine, 'degree'):
            Base.metadata.tables['degree'].create(engine)
            logger.info("table created")
            # print("table created in database")

        degree = convert_list_to_str(data['degree']).strip()
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


def insert_into_degree_level(data, inst_param_group_level, inst_param_value_level):
    logger.info("inserting into Degree_level table")
    global degree_id, level_id
    try:
        if not table_exists(engine, 'degree_level'):
            Base.metadata.tables['degree_level'].create(engine)
            logger.info("table created")
        degree = convert_list_to_str(data['degree']).strip()
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
                # print("degree data Inserted")
                session.close()
        except Exception as e:
            print("error while inserting data into degree-level ", e)
            pass
    except Exception as e:
        session.rollback()
        logger.debug("Error raised in insert_into_degree_level(): %s" % e)
        pass


def insert_into_location(data):
    logger.info("inserting into Location table")
    global inst_id
    try:
        if not table_exists(engine, 'location'):
            Base.metadata.tables['location'].create(engine)
            logger.info("table created")
            # print("table created in database")
        try:
            for location in data['location']:
                try:
                    external_id = hashlib.md5((location.strip()).encode('utf-8')).hexdigest()
                    count = session.query(Location.external_id).where(Location.external_id == external_id).all()
                    if len(count) > 0:
                        logger.info("Duplicate record found")
                    else:
                        location_table = Location(str(uuid.uuid4()), external_id, location, None, datetime.now(),
                                                  created_by[0], datetime.now(), updated_by[0])
                        session.add(location_table)
                        session.commit()
                        logger.info("data inserted into location table")
                        session.close()
                except Exception as e:
                    session.rollback()
                    logger.debug("Error raised as: %s" % e)
                    pass
        except Exception as e:
            pass
            logger.debug("Error :no location found : %s" % e)
    except Exception as e:
        session.rollback()
        logger.debug("Error raised, insert-into-location() : %s" % e)
        pass


def insert_into_program(soup, program_url, get_degree, data, prog_level, prog_type, inst_id, program_location, program_description):
    logger.info("inserting into program table")
    global get_prog_level_id, degree_id, add_prog_fee, second_lang_req, math_intensity
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
            degree_id = session.query(Degree.id).filter(Degree.name == get_degree).one()
            session.commit()
        except Exception as e:
            session.rollback()
            pass
        try:
            if data['Additional_Program_Fee']:
                fee = data['Additional_Program_Fee'].split(":")[1].strip()
                add_prog_fee = get_boolean(fee)
            else:
                add_prog_fee = None
        except Exception as e:
            add_prog_fee = None
            pass
        try:
            if data['Second_Language_Requirement']:
                s_language = data['Second_Language_Requirement'].split(":")[1].strip()
                second_lang_req = get_boolean(s_language)
            else:
                second_lang_req = None
        except Exception as e:
            second_lang_req = None
            pass

        first_req_math_course_id = None
        try:
            if data['Math_Intensity']:
                math_intensity = find_math_intensity(data['Math_Intensity'])
            else:
                math_intensity = None
        except Exception as e:
            math_intensity = None
            pass
        try:
            if yaml_obj.get(Website_URL).get('DEGREE_TYPE') == 'Bachelor':
                if "Online" in program_location:
                    get_attend_online_des = soup.findAll('div', {'class': 'mobileRow row mobile-toggle-content'})[7]
                    attend_online = html_text.extract_text(f"{get_attend_online_des}")

                else:
                    attend_online = None
            else:
                if "Online" in program_location:
                    check_requirement = soup.findAll('div', {'class': 'mobileRow row'})[4]
                    get_requirement_text = html_text.extract_text(f"{check_requirement}")
                    if get_requirement_text == 'Accelerated Program Options ▲':
                        get_attend_online_des = soup.findAll('div', {'class': 'mobileRow row mobile-toggle-content'})[6]
                        attend_online = html_text.extract_text(f"{get_attend_online_des}")
                    else:
                        get_attend_online_des = soup.findAll('div', {'class': 'mobileRow row mobile-toggle-content'})[5]
                        attend_online = html_text.extract_text(f"{get_attend_online_des}")
                    # attend_online = re.sub('\s\s\s','',soup.findAll('div', {'class': 'mobileRow row mobile-toggle-content'})[7].text)
                    # attend_online = data['Attend_online']
                else:
                    attend_online = None
        except Exception as e:
            attend_online = None
        program_title = data['Program_title'].split(",")
        try:
            uniq_id = str(uuid.uuid4())
            external_id = hashlib.md5(program_url.encode('utf-8')).hexdigest()
            count = session.query(Program.external_id).where(Program.external_id == external_id).all()
            if len(count) > 0:
                logger.info("Duplicate record found")
            else:
                program_table = Program(uniq_id, external_id, get_prog_level_id[0], degree_id[0], inst_id[0],
                                        data['Program_code'], program_title[0].strip(), program_description,
                                        add_prog_fee, second_lang_req, first_req_math_course_id, math_intensity,
                                        program_url, None, None, None, attend_online, datetime.now(), created_by[0],
                                        datetime.now(), updated_by[0])
                session.add(program_table)
                session.commit()
                logger.info("data inserted into program table")
                session.close()
        except Exception as e:
            logger.debug("Error raised while inserting into program: %s" % e)
    except Exception as e:
        session.rollback()
        logger.debug("Error raised in insert-into-program() :%s" % e)
        # print("Error :", e)
        pass


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


def send_graduate_to_req_table(soup, program_url, data, program_id, inst_id):
    global rmqt_group_id, req_cat_degree_title, req_category_id
    print("inserting graduate degree each requirements..!")
    # Data will be inserting into Requirement table
    check_requirement = soup.findAll('div', {'class': 'mobileRow row'})[4]
    get_requirement_text = html_text.extract_text(f"{check_requirement}")
    if get_requirement_text == 'Accelerated Program Options ▲':
        get_req = soup.findAll('div', {'class': 'mobileRow row mobile-toggle-content'})[4]
    else:
        get_req = soup.findAll('div', {'class': 'mobileRow row mobile-toggle-content'})[3]
    get_all_paragraph = get_req.find_all('p')
    # data = soup.find('div', {'class': "mobileCell cell"})
    total_credits = re.findall(r'\d+', get_req.find_all('p')[0].text)
    deg_title = get_req.findAll('strong')
    program_title = data['Program_title'].split(",")[0]
    url = program_url + program_title

    try:
        uniq_id = str(uuid.uuid4())
        external_id = hashlib.md5(url.encode('utf-8')).hexdigest()
        count = session.query(Requirement_group.external_id).where(Requirement_group.external_id == external_id).all()
        if len(count) > 0:
            logger.info("Duplicate record found")
        else:
            requirement_group_table = Requirement_group(uniq_id, external_id, program_id[0], program_title,
                                                        None, 'Hours', int(total_credits[0]), None, None, None, None,
                                                        None, None, None, None,None, None, None, None,program_url, None,
                                                        None, None, datetime.now(),created_by[0],datetime.now(), updated_by[0])
            session.add(requirement_group_table)
            session.commit()
            logger.info("data inserted into requirement_group")
            session.close()
    except Exception as e:
        session.rollback()
        print("Error raised as while insert to Requirement_group-613 as: ", e)
    try:
        insert_into_term(program_url, None, "Term 1", None, None)
    except Exception as e:
        print("error raised while inserting-into-term as:", e)
    try:  # Entering Degree-requirement-category to rmqt-catefory table
        rmqt_group_external_id = hashlib.md5(url.encode('utf-8')).hexdigest()
        rmqt_group_id = session.query(Requirement_group.id).where(
            Requirement_group.external_id == rmqt_group_external_id).first()
        for title in deg_title:
            uniq_id = str(uuid.uuid4())
            # external_id = hashlib.md5(str(program_url + title.text).encode('utf-8')).hexdigest()

            get_text = title.text.split("(")[0]
            external_id = hashlib.md5(str(get_text).encode('utf-8')).hexdigest()
            count = session.query(Graduate_req_category.external_id).where(
                Graduate_req_category.external_id == external_id).all()
            # get_text = title.text.split("(")[0]
            try:
                if len(count) > 0:
                    logger.info("Duplicate record found")
                else:
                    Graduate_deg_table = Graduate_req_category(uniq_id, external_id, inst_id[0], get_text, datetime.now(),
                                                               created_by[0], datetime.now(), updated_by[0])
                    session.add(Graduate_deg_table)
                    session.commit()
                    logger.info("data inserted into Graduate_requirement_group table")
                    session.close()
            except Exception as e:
                print("Error raised while entering into requirement-category table :", e)
            # inserting into Requirement_group_Requirement_category table
            try:
                req_category_id = session.query(Graduate_req_category.id).where(Graduate_req_category.external_id == external_id).first()
                get_category_credits = re.findall(r'\d+', title.text)
                try:
                    if len(get_category_credits) > 1:
                        min_cat_credits = int(get_category_credits[0])
                        max_cat_credits = int(get_category_credits[1])
                    else:
                        min_cat_credits = None
                        max_cat_credits = int(get_category_credits[0])
                except Exception as e:
                    min_cat_credits = None
                    max_cat_credits = None

                if max_cat_credits is None and min_cat_credits is None:
                    credit_type = None
                else:
                    credit_type = 'Hours'
                Rqmt_grp_rqmt_category_table = Rqmt_group_rqmt_category(rmqt_group_id[0], req_category_id[0],
                                                                        credit_type, min_cat_credits, max_cat_credits)
                session.add(Rqmt_grp_rqmt_category_table)
                session.commit()
                logger.info("data inserted into program table")
                session.close()
            except Exception as e:
                session.rollback()
                print("Error raised as Requirement_group_Requirement_category-table as:", e)

    except Exception as e:
        session.rollback()
        print("Error raised while entering degree category into table: ", e)
    for para in get_all_paragraph:
        try:
            if para.text != "":
                # if len(para.findAll('br')) > 0:
                try:
                    degree_title = para.strong.text
                    req_cat_degree_title = degree_title.split("(")[0]
                except Exception as e:
                    degree_title = ""
                if degree_title != "":
                    try:
                        if len(para.findAll('br')) > 0:
                            for req in para.findAll('br'):
                                requirement = req.next
                                uniq_id = str(uuid.uuid4())
                                # req_category_id = session.query(Graduate_req_category.id).filter(Graduate_req_category.name == req_cat_degree_title).first()
                                req_category_id = session.query(Graduate_req_category.id).where(Graduate_req_category.name == req_cat_degree_title).first()

                                try:
                                    max_credits = re.findall('(?<!\d)\d(?!\d)', requirement)
                                    max_credits = int(max_credits[0])
                                    credit_type = 'Hours'
                                except Exception as e:
                                    max_credits = None
                                    credit_type = None

                                requirement_text_1 = re.sub(r'(?<!\d)\d(?!\d)', ' ', requirement)
                                requirement_text = re.sub('[\n()\n]', ' ', requirement_text_1)
                                req_group_req_category_id = session.query(Rqmt_group_rqmt_category.id).where(
                                    Rqmt_group_rqmt_category.rqmt_category_id == req_category_id[0] and
                                    Rqmt_group_rqmt_category.rqmt_group_id == rmqt_group_id[0]).first()
                                external_id = hashlib.md5(str(program_url + requirement).encode('utf-8')).hexdigest()
                                count = session.query(Requirement.external_id).where(
                                    Requirement.external_id == external_id).all()
                                if len(count) > 0:
                                    logger.info("Duplicate record found")
                                else:
                                    try:
                                        Requirement_table = Requirement(uniq_id, external_id, rmqt_group_id[0],
                                                                        req_group_req_category_id[0],
                                                                        requirement_text, None, credit_type, None,
                                                                        max_credits, None, None, None,
                                                                        datetime.now(), created_by[0], datetime.now(),
                                                                        updated_by[0])
                                        session.add(Requirement_table)
                                        session.commit()
                                        logger.info("data inserted into program table")
                                        session.close()
                                    except Exception as e:
                                        session.rollback()
                                        print("error raised as :", e)
                                try:
                                    # insert into Requirement-term table
                                    req_table_id = session.query(Requirement.id).where(
                                        Requirement.external_id == external_id).first()
                                    external_id = hashlib.md5(
                                        str(str(requirement_group_id[0]) + "Term 1").encode('utf-8')).hexdigest()
                                    # term_id = session.query(Term.id).where(Term.name == "Term 1").first()
                                    term_id = session.query(Term.id).where(Term.external_id == external_id).first()
                                    requirement_term_table = Requirement_term(req_table_id[0], term_id[0])
                                    session.add(requirement_term_table)  # persists data
                                    session.commit()  # commit and close session
                                    logger.info("data inserted into requirement_term ")
                                    session.close()
                                except Exception as e:
                                    session.rollback()
                                    print("error raised as :", e)

                                try:
                                    # insert-into-course_summary
                                    get_requirement = re.findall(r'\S+', requirement)
                                    course_sub_prefix = get_requirement[0]
                                    course_sub_sufix = get_requirement[1]
                                    if course_sub_sufix.isdigit():
                                        get_url = furl(
                                            'https://webapp4.asu.edu/catalog/courselist?s=ACT&n=593&t=2227&hon=F&gg=F')
                                        get_new_link = get_url.set(
                                            {"s": course_sub_prefix, "n": course_sub_sufix, "t": "2227", "hon": "F",
                                             "gg": "F"})
                                        get_link = get_new_link.url
                                        scrape_course_curriculum_page(get_link, requirement, requirement, inst_id)
                                        try:
                                            # inserting into requirement_variable
                                            uniq_id = str(uuid.uuid4())
                                            course_ext_id = hashlib.md5(
                                                str(get_link + requirement).encode('utf-8')).hexdigest()
                                            get_req_table_external_id = hashlib.md5(
                                                str(program_url + requirement).encode('utf-8')).hexdigest()
                                            get_req_id = session.query(Requirement.id).where(
                                                Requirement.external_id == get_req_table_external_id).first()
                                            entity = 'course'
                                            subject_code = course_sub_prefix + " " + course_sub_sufix
                                            value_id = session.query(Course.id).where(
                                                Course.code == subject_code).first()
                                            requirement_text_1 = re.sub(r'(?<!\d)\d(?!\d)', ' ', requirement)
                                            requirement_text = re.sub('[\n()\n]', ' ', requirement_text_1)
                                            # print("requirement-text: ", requirement_text, "\n")
                                            post_data_into_rqmt_variable(uniq_id, course_ext_id, get_req_id[0],
                                                                         requirement_text, entity, value_id[0])
                                        except Exception as e:
                                            print("Error raised data_into_rqmt_variable-695 as: ", e)
                                except Exception as e:
                                    print("Error raised insert-into-course_summary-696 as: ", e)

                        else:
                            # inserting Degree category into requirements
                            uniq_id = str(uuid.uuid4())
                            req_category_id = session.query(Graduate_req_category.id).where(Graduate_req_category.name == req_cat_degree_title).first()
                            req_group_req_category_id = session.query(Rqmt_group_rqmt_category.id).where(
                                Rqmt_group_rqmt_category.rqmt_category_id == req_category_id[0] and
                                Rqmt_group_rqmt_category.rqmt_group_id == rmqt_group_id[0]).first()
                            get_degree_title = degree_title.split("(")[0].strip()
                            try:
                                max_credits = re.findall(r'\d+', degree_title)
                                if len(max_credits) > 1:
                                    min_credits = int(max_credits[0])
                                    max_credits = int(max_credits[1])
                                else:
                                    min_credits = None
                                    max_credits = int(max_credits[0])
                            except Exception as e:
                                min_credits = None
                                max_credits = None
                            external_id = hashlib.md5(str(program_url + degree_title).encode('utf-8')).hexdigest()
                            count = session.query(Requirement.external_id).where(Requirement.external_id == external_id).all()
                            if len(count) > 0:
                                logger.info("Duplicate record found")
                            else:
                                try:
                                    Requirement_table = Requirement(uniq_id, external_id, rmqt_group_id[0],
                                                                    req_group_req_category_id[0],get_degree_title, None,
                                                                    'Hours',min_credits,max_credits, None, None, None,
                                                                    datetime.now(), created_by[0], datetime.now(),
                                                                    updated_by[0])
                                    session.add(Requirement_table)
                                    session.commit()
                                    logger.info("data inserted into program table")
                                    session.close()
                                except Exception as e:
                                    session.rollback()
                                    print("error raised at line-750 as :", e)

                            try:
                                # insert into Requirement-term table
                                req_table_id = session.query(Requirement.id).where(
                                    Requirement.external_id == external_id).first()
                                term_id = session.query(Term.id).where(Term.name == "Term 1").first()
                                requirement_term_table = Requirement_term(req_table_id[0], term_id[0])
                                session.add(requirement_term_table)  # persists data
                                session.commit()  # commit and close session
                                logger.info("data inserted into requirement_term ")
                                session.close()
                            except Exception as e:
                                session.rollback()
                                print("error raised as :", e)
                            try:
                                # inserting into requirement_variable
                                get_degree_title = degree_title.split("(")[0].strip()
                                uniq_id = str(uuid.uuid4())
                                course_ext_id = hashlib.md5(str(program_url + degree_title).encode('utf-8')).hexdigest()
                                get_req_table_external_id = hashlib.md5(
                                    str(program_url + degree_title).encode('utf-8')).hexdigest()
                                get_req_id = session.query(Requirement.id).where(
                                    Requirement.external_id == get_req_table_external_id).first()
                                entity = 'elective'
                                value_id = None
                                post_data_into_rqmt_variable(uniq_id, course_ext_id, get_req_id[0], get_degree_title,
                                                             entity, value_id)
                            except Exception as e:
                                print("Error raised data_into_rqmt_variable-762 as: ", e)
                    except Exception as e:
                        print("error raised while gathering req : ", e)
                else:
                    requirement = para.text

                    max_credits = None
                    uniq_id = str(uuid.uuid4())
                    external_id = hashlib.md5(str(program_url + requirement).encode('utf-8')).hexdigest()
                    count = session.query(Requirement.external_id).where(Requirement.external_id == external_id).all()
                    if len(count) > 0:
                        logger.info("Duplicate record found")
                    else:
                        try:
                            Requirement_table = Requirement(uniq_id, external_id, rmqt_group_id[0], None,
                                                            requirement, None, None, None, max_credits, None, None,
                                                            None,datetime.now(), created_by[0], datetime.now(),
                                                            updated_by[0])
                            session.add(Requirement_table)
                            session.commit()
                            logger.info("data inserted into program table")
                            session.close()
                        except Exception as e:
                            session.rollback()
                            print("error raised as :", e)

                # print("Requirement: ", requirement)
        except Exception as e:
            print("error raised as:", e)


def get_graduate_admission_req(soup, program_url, data, program_id):
    try:
        if not table_exists(engine, 'admission_req'):
            Base.metadata.tables['admission_req'].create(engine)
            logger.info("table created")
        check_requirement = soup.findAll('div', {'class': 'mobileRow row'})[4]
        get_requirement_text = html_text.extract_text(f"{check_requirement}")
        if get_requirement_text == 'Accelerated Program Options ▲':
            get_admission_description = soup.findAll('div', {'class': 'mobileRow row mobile-toggle-content'})[5]
        else:
            get_admission_description = soup.findAll('div', {'class': 'mobileRow row mobile-toggle-content'})[4]
        admission_description = html_text.extract_text(f"{get_admission_description}")

        # get_req = soup.findAll('div', {'class': 'mobileRow row mobile-toggle-content'})[5].text
        # collect_adm_text = re.sub('\s\s\s', "", get_req)
        uniq_id = str(uuid.uuid4())

        external_id = hashlib.md5(str(program_url + admission_description).encode('utf-8')).hexdigest()
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
                session.rollback()
                print("error raised as Admission_req_table in :", e)
        # get_all_paragraph = get_req.find_all('p')
        # get_list = get_req.find('ol').text
        # for each_para in get_all_paragraph:
        #     if each_para == get_all_paragraph[3]:
        #         each_adm_req = each_para.text + get_list
        #     else:
        #         each_adm_req = each_para.text
        #     uniq_id = str(uuid.uuid4())
        #
        #     external_id = hashlib.md5(str(program_url + each_para.text).encode('utf-8')).hexdigest()
        #     count = session.query(Requirement.external_id).where(Requirement.external_id == external_id).all()
        #     if len(count) > 0:
        #         logger.info("Duplicate record found")
        #     else:
        #         try:
        #             Admission_req_table = Admission_req(uniq_id, external_id, program_id[0], each_adm_req,
        #                                                 datetime.now(), created_by[0], datetime.now(), updated_by[0])
        #             session.add(Admission_req_table)
        #             session.commit()
        #             logger.info("data inserted into program table")
        #             session.close()
        #         except Exception as e:
        #             session.rollback()
        #             print("error raised as Admission_req_table in :", e)
    except Exception as e:
        print("error raised in Admission_req_table as :", e)
        print("No Admission_req to scrape")


def insert_into_inst_location(inst_id, program_location):
    print("Inserting into institution-location table")
    try:
        if not table_exists(engine, 'institution_location'):
            Base.metadata.tables['institution_location'].create(engine)
            logger.info("table created")
        try:
            for id in program_location:
                prog_location = session.query(Location.id).where(Location.name == id).one()
                Institution_location_table = Institution_location(inst_id[0], prog_location[0])
                session.add(Institution_location_table)  # persists data
                session.commit()  # commit and close session
                logger.info("data inserted into institution-location table")
                session.close()
            session.commit()
        except Exception as e:
            session.rollback()
            logger.debug("duplicate data found in institution-location(): ")
            pass

    except Exception as e:
        session.rollback()
        logger.debug("error found in institution-location %s" % e)
        # print("duplicate found in program_location: ", e)
        pass


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


def insert_into_program_location(program_url, location, program_id):
    logger.info("inserting into program_location")
    global prog_location
    try:
        if not table_exists(engine, 'program_location'):
            Base.metadata.tables['program_location'].create(engine)
            logger.info("table created")
            # print("table created in database")
        try:
            for id in location:
                prog_location = session.query(Location.id).where(Location.name == id).one()
                program_location_table = Program_location(program_id[0], prog_location[0])
                session.add(program_location_table)  # persists data
                session.commit()  # commit and close session
                logger.info("data inserted into program_location")
                session.close()
            session.commit()
        except Exception as e:
            session.rollback()
            logger.debug("duplicate data found in program_location: ")
            pass

    except Exception as e:
        session.rollback()
        logger.debug("error found in program_location %s" % e)
        # print("duplicate found in program_location: ", e)
        pass


def get_location_type(value):
    list = ['Tempe campus', 'Polytechnic campus', 'West', 'West campus', 'Downtown Phoenix campus', 'The Gila Valley',
            'Havasu', 'Los Angeles', " "]
    if any(x in list for x in value):
        return 'oncampus'
    else:
        return 'online'


def insert_into_requirement_group(program_id, program_url, program_title, url, ex_data, total_credits, upper_dev_min,
                                  upper_dev_credits, tot_cred_at_prov_min, tot_cred_at_prov, resi_cred_min,
                                  resi_credits, tot_comm_coll_cred_min, tot_comm_coll_cred, major_gpa_min, major_gpa,
                                  cumulative_gpa_min, cumulative_gpa):
    logger.info("inserting into requirement_group table")
    try:
        if not table_exists(engine, 'rqmt_group'):
            Base.metadata.tables['rqmt_group'].create(engine)
            logger.info("table created in database")
        progam_name = ex_data['Program_name'].split(",")[0]
        get_type = get_location_type(ex_data['Location_type'])
        external_link = url
        get_academic_year = re.findall(r"\d+", ex_data['Program_year'])
        academic_year = get_academic_year[0] + " - " + get_academic_year[1]
        start_year = int(get_academic_year[0])
        end_year = int(get_academic_year[1])
        uniq_id = str(uuid.uuid4())
        external_id = hashlib.md5(external_link.encode('utf-8')).hexdigest()
        count = session.query(Requirement_group.external_id).where(Requirement_group.external_id == external_id).all()
        if len(count) > 0:
            logger.info("Duplicate record found")
        else:
            requirement_group_table = Requirement_group(uniq_id, external_id, program_id[0], progam_name.strip(),
                                                        get_type, 'Hours', total_credits, upper_dev_min,
                                                        upper_dev_credits, tot_cred_at_prov_min, tot_cred_at_prov,
                                                        resi_cred_min, resi_credits,
                                                        tot_comm_coll_cred_min, tot_comm_coll_cred, major_gpa_min,
                                                        major_gpa, cumulative_gpa_min,
                                                        cumulative_gpa, external_link, academic_year,start_year, end_year , datetime.now(), created_by[0],
                                                        datetime.now(), updated_by[0])
            session.add(requirement_group_table)
            session.commit()
            logger.info("data inserted into requirement_group")
            session.close()
    except Exception as e:
        session.rollback()
        logger.debug("Error raised in Requirement_group: %s" % e)
        # print("Error raised in Requirement_group:", e)
        pass


def insert_into_term(url, program_year, term_head, course_hour, total_hours):
    logger.info("inserting into term table")
    global requirement_group_id, part, total_hours_max
    try:
        if not table_exists(engine, 'term'):
            Base.metadata.tables['term'].create(engine)
            logger.info("table created")
        try:
            requirement_group_id = session.query(Requirement_group.id).filter(
                Requirement_group.external_link == url).one()
            session.commit()
        except Exception as e:
            session.rollback()
            logger.debug("Error: No id found: %s" % e)
            pass
        try:
            term = term_head.split("-")
            if len(term) > 1:
                main = term[0]
                part = term[1]
            else:
                main = term[0]
                part = None
        except Exception as e:
            main = None
            part = None
        try:
            year = re.findall(r'[\d\.\d]+', program_year)
            year = int(year[1]) - int(year[0])
        except Exception as e:
            year = None
        try:
            if len(total_hours) > 1:
                total_hours_min = int(float(total_hours[0]))
                total_hours_max = int(float(total_hours[1]))
            else:
                total_hours_min = None
                total_hours_max = int(float(total_hours[0]))
        except Exception as e:
            total_hours_min = None
            total_hours_max = None
            pass
        try:
            if len(course_hour) > 1:
                min_credit = int(float(course_hour[0]))
                max_credit = int(float(course_hour[1]))
            else:
                min_credit = None
                max_credit = int(float(course_hour[0]))
        except Exception as e:
            min_credit = None
            max_credit = None

        uniq_id = str(uuid.uuid4())
        external_id = hashlib.md5(str(str(requirement_group_id[0]) + term_head).encode('utf-8')).hexdigest()
        count = session.query(Term.external_id).where(Term.external_id == external_id).all()
        if len(count) > 0:
            logger.info("Duplicate record found")
        else:
            term_table = Term(uniq_id, external_id, requirement_group_id[0], term_head, main, part, 'Hours', min_credit,
                              max_credit, total_hours_min, total_hours_max, year, datetime.now(), created_by[0],
                              datetime.now(),
                              updated_by[0])
            session.add(term_table)
            session.commit()
            logger.info("data inserted into term table")
            session.close()
    except Exception as e:
        session.rollback()
        logger.debug("Error in insert_into_term(), %s" % e)
        pass
    return requirement_group_id


def insert_into_rqmt_group_college(rqmt_group_id, college_name):
    try:
        print("inserting into Rqmt_group_college()")
        if not table_exists(engine, 'rqmt_group_college'):
            Base.metadata.tables['rqmt_group_college'].create(engine)
            logger.info("table created")

        college_id = session.query(Institution.id).where(Institution.name == college_name).first()
        rqmt_group_college_table = Rqmt_group_college(rqmt_group_id[0], college_id[0])
        session.add(rqmt_group_college_table)
        session.commit()
        logger.info("data inserted into Rqmt_group_college table")
        session.close()

    except Exception as e:
        session.rollback()
        logger.debug("Error for Rqmt_group_college(): %s" % e)


def insert_into_rqmt_group_location(rqmt_group_id, location_name):
    try:
        print("inserting into Rqmt_group_location() table")
        if not table_exists(engine, 'rqmt_group_location'):
            Base.metadata.tables['rqmt_group_location'].create(engine)
            logger.info("table created")

        get_all_location = session.query(Location.name).all()
        all_location_list = []
        for i in get_all_location:
            all_location_list.append(i[0])
        for location in all_location_list:
            for check_loc in location_name:
                if location in check_loc:
                    location_id = session.query(Location.id).where(Location.name == location).first()
                    rqmt_group_location_table = Rqmt_group_location(rqmt_group_id[0], location_id[0])
                    session.add(rqmt_group_location_table)
                    session.commit()
                    logger.info("data inserted into Rqmt_group_location table")
                    session.close()

    except Exception as e:
        session.rollback()
        logger.debug("Error for Rqmt_group_location(): %s" % e)


def insert_into_requirement(requirement_group_id, term_head, program_title, location, rqmnt_group_ext_link,
                            subject_raw_text, subject,
                            subject_link, subject_hours, subj_minimum_grade, critical_course, necessary_course):
    logger.info("inserting into requirement table")
    global max_credits, minimum_grade
    logger.debug("rqmnt-link: %s" % rqmnt_group_ext_link)
    logger.debug("program_title: %s" % program_title)
    try:
        if not table_exists(engine, 'requirement'):
            Base.metadata.tables['requirement'].create(engine)
            logger.info("table created")

        uniq_id = str(uuid.uuid4())
        ext_group_text = term_head + program_title + convert_list_to_str(location) + subject_raw_text
        external_id = hashlib.md5(ext_group_text.encode('utf-8')).hexdigest()
        count = session.query(Requirement.external_id).where(Requirement.external_id == external_id).all()
        if len(count) > 0:
            # print("Duplicate record found")
            logger.info("Duplicate record found")
        else:
            if len([subject_hours]) > 1:
                min_credits = int(float(subject_hours[0].strip()))
                max_credits = int(float(subject_hours[1].strip()))
            else:
                min_credits = None
                max_credits = int(float(subject_hours[0].strip()))
            requirement_table = Requirement(uniq_id, external_id, requirement_group_id[0], None, subject_raw_text, None,
                                            'Hours', min_credits, max_credits, subj_minimum_grade, critical_course,
                                            necessary_course, datetime.now(), created_by[0], datetime.now(),
                                            updated_by[0])
            session.add(requirement_table)
            session.commit()
            logger.info("data inserted into requirement table")
            session.close()
    except Exception as e:
        session.rollback()
        logger.debug("Error for insert_into_requirement(): %s" % e)
        pass


def insert_into_requirement_1(requirement_group_id, term_head, program_title, location, rqmnt_group_ext_link,
                              subject_raw_text, subject,
                              subject_link, subject_hours, subj_minimum_grade, critical_course, necessary_course):
    logger.info("inserting into requirement_1")
    global max_credits, minimum_grade
    try:
        uniq_id = str(uuid.uuid4())
        ext_group_text = term_head + program_title + convert_list_to_str(location) + subject_raw_text
        external_id = hashlib.md5(ext_group_text.encode('utf-8')).hexdigest()
        count = session.query(Requirement.external_id).where(Requirement.external_id == external_id).all()
        if len(count) > 0:
            logger.info("Duplicate record found")
        else:
            requirement_table = Requirement(uniq_id, external_id, requirement_group_id[0], None, subject_raw_text, None,
                                            None, None, None, None, critical_course, necessary_course,
                                            datetime.now(), created_by[0], datetime.now(), updated_by[0])
            session.add(requirement_table)
            session.commit()
            logger.info("data inserted into requirement table")
            session.close()
    except Exception as e:
        session.rollback()
        logger.debug("Error for insert_into_requirement(): %s" % e)
        pass


def insert_into_requirement_term(requirement_group_id, rqmt_group_ext_link, program_title, location, term_head,
                                 subject_raw_text):
    logger.info("inserting intorequirement_term table ")
    global requirement_id, term_id
    try:
        if not table_exists(engine, 'rqmt_term'):
            Base.metadata.tables['rqmt_term'].create(engine)
            logger.info("table created")

        try:
            ext_group_text = term_head + program_title + convert_list_to_str(location) + subject_raw_text
            external_id = hashlib.md5(ext_group_text.encode('utf-8')).hexdigest()

            sub_req = session.query(Requirement_group.id).where(
                Requirement_group.external_link == rqmt_group_ext_link).one()
            requirement_id = session.query(Requirement.id).where(Requirement.external_id == external_id).where(
                Requirement.rqmt_group_id.in_(sub_req)).one()

            sub_req = session.query(Requirement_group.id).where(
                Requirement_group.external_link == rqmt_group_ext_link).one()
            external_term_id = hashlib.md5(str(str(sub_req[0]) + term_head).encode('utf-8')).hexdigest()
            term_id = session.query(Term.id).where(Term.external_id == external_term_id).where(
                Term.requirement_group_id.in_(sub_req)).one()
        except Exception as e:
            session.rollback()
            logger.debug("No mapping id found in requirement_term: %s" % e)
            # print("No id found in requirement_term: ")
            pass

        requirement_term_table = Requirement_term(requirement_id[0], term_id[0])
        session.add(requirement_term_table)  # persists data
        session.commit()  # commit and close session
        logger.info("data inserted into requirement_term ")
        session.close()
    except Exception as e:
        session.rollback()
        logger.debug("Duplicate id found in requirement_term ")
        # print("Duplicate id found in requirement_term ")
        pass


def insert_into_course(soup, subject_link, course_code, sub_title, sub_title_link, desciption, course_credit, gs,
                       expression, inst_id):
    logger.info("inserting into course table")
    global general_studies, course_soup, summary_data, code, title, code_suffix, get_gs, course_level_id
    if not table_exists(engine, 'course'):
        Base.metadata.tables['course'].create(engine)
        logger.info("table created")
        # print("table created in database")
    try:
        course_title = sub_title.strip()
        course_code = course_code.strip()
        get_course_code = re.findall(r'\S+', course_code)
        general_studies = gs.strip()
        code_prefix = get_course_code[0].strip()
        code_suffix = get_course_code[1].strip()
        course_level_list = ['Lower division', 'Upper division', 'Graduate']
        try:
            if int(code_suffix) in range(100, 299):
                print("number found in range (100-299) as Lower division:", code_suffix)
                course_level_id = session.query(Inst_param_value.id).filter(Inst_param_value.name == 'Lower division').first()
            if int(code_suffix) in range(300, 499):
                print("number found in range (101-299) as Upper division:", code_suffix)
                course_level_id = session.query(Inst_param_value.id).filter(Inst_param_value.name == 'Upper division').first()
            if int(code_suffix) in range(500, 10000):
                print("number found in range (300-499) as Graduate:", code_suffix)
                course_level_id = session.query(Inst_param_value.id).filter(Inst_param_value.name == 'Graduate').first()
        except Exception as e:
            print("error raised while getting course-level-id as :", e)
            course_level_id = None
        try:
            units = course_credit.split("-")
            if len(units) > 1:
                min_credit = int(float(units[0]))
                max_credit = int(float(units[1]))
                credit = 1
            else:
                min_credit = None
                max_credit = int(units[0])
                credit = 1
        except Exception as e:
            # print("No units found.")
            min_credit = None
            max_credit = None
            credit = 0

        try:
            if general_studies:
                general_studies = general_studies.strip()
                # print("length id Gs:", len(general_studies))
            else:
                general_studies = None
        except Exception as e:
            general_studies = None
            logger.info("No General_Studies data found")
            # print("No General_Studies data found")
            pass
        uniq_id = str(uuid.uuid4())
        external_id = hashlib.md5(course_code.encode('utf-8')).hexdigest()
        count = session.query(Course.external_id).where(Course.external_id == external_id).all()
        try:
            if len(count) > 0:
                # print("Duplicate record found")
                logger.info("Duplicate record found")
            else:
                course_table = Course(uniq_id, external_id, inst_id[0], course_title, course_code, code_prefix, int(code_suffix), None,
                                      desciption, credit, "Hours", min_credit, max_credit, sub_title_link,
                                      general_studies, None, course_level_id[0], datetime.now(), created_by[0], datetime.now(), updated_by[0])
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

        # map the data into course_gs_category
        try:
            try:
                fetch_gs = re.sub("[(,|,&,or,)]", ',', general_studies)
                a = fetch_gs.replace(" ", "")
                get_gs = a.split(",")  # list
            except Exception as e:
                logger.debug("no general studies for : %s" % course_title)
                # print("no general studies for :", course_title)
                pass

            if expression is not None:
                logger.info("calling course_gs_category ")
                # print('inserting values: ', expression, ",",  general_studies, "\n")
                insert_into_course_gs_category(course_code, course_title, expression, get_gs)
            else:
                logger.info("No course_gs category for :%s" % course_title)
                # print("No course_gs category found,", "\n")
        except Exception as e:
            logger.info("Error raised while calling course_gs_category in course table %s" % e)
            pass

        session.close()
    except Exception as e:
        logger.info("Error raised in insert_into_course(): %s" % e)
        pass


def calling_insert_into_course_college(course_code):
    sub_course_code = re.findall(r'\S+', course_code)
    course_sub_prefix = sub_course_code[0]
    course_sub_sufix = sub_course_code[1]
    get_url = furl(
        'https://webapp4.asu.edu/catalog/courselist?s=ACT&n=593&t=2227&hon=F&gg=F')
    get_new_link = get_url.set(
        {"s": course_sub_prefix, "n": course_sub_sufix, "t": "2227", "hon": "F",
         "gg": "F"})
    get_link = get_new_link.url
    driver.get(get_link)
    time.sleep(4)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    course_college_data = extract_data_using_selector_lib(soup, "Post_curriculum_summary_1", Website_URL)
    try:
        insert_into_course_college(course_code, course_college_data)
    except Exception as e:
        print("Error while calling course college-0")
        pass


def insert_into_course_college(course_code, data):
    global college_id
    print("calling course-college table & course-code is:", course_code)
    if not table_exists(engine, 'course_college'):
        Base.metadata.tables['course_college'].create(engine)
        logger.info("table created")
    try:
        course_id = session.query(Course.id).where(Course.code == course_code.strip()).first()
        course_course_id = session.query(Course_college.course_id).where(Course_college.course_id == course_id[0]).all()
        if len(course_course_id) > 0:
            print("Duplicate record found in course-college table")
        else:
            if len(data['course_college_dept']) <= 1:
                if data['course_prerequisites'][0] == "":
                    data['course_prerequisites'] = None
                else:
                    data['course_prerequisites'] = data['course_prerequisites'][0]
                if data['course_college_dept'][0] != "":
                    get_college = data['course_college_dept'][0].split("--")
                    college_name = get_college[0].strip()
                    dept_name = get_college[1].strip()
                else:
                    college_name = None
                    dept_name = None
                college_id = session.query(Institution.id).where(Institution.name == college_name.strip()).all()
                try:
                    post_course_college_data(course_code, course_id, college_id, college_name,
                                             data['course_prerequisites'], dept_name)
                except Exception as e:
                    print("Error while calling post_course_college_data-1", e)
                    pass
            else:
                try:
                    for get_college, prerequisities in zip(data['course_college_dept'], data['course_prerequisites']):
                        get_college = get_college.split("--")
                        college_name = get_college[0].strip()
                        dept_name = get_college[1].strip()
                        if prerequisities == "":
                            collect_prerequisities = None
                        else:
                            collect_prerequisities = prerequisities
                        college_id = session.query(Institution.id).where(Institution.name == college_name).all()
                        try:
                            post_course_college_data(course_code, course_id, college_id, college_name,
                                                     collect_prerequisities, dept_name)
                        except Exception as e:
                            print("Error while calling post_course_college_data-2", e)
                            pass
                        # try:
                        #     for prerequisities in data['course_prerequisites']:
                        #         post_course_college_data(course_code,course_id, college_id, college_name, prerequisities, dept_name)
                        # except Exception as e:
                        #     prerequisities = None
                        #     post_course_college_data(course_code,course_id, college_id, college_name, prerequisities, dept_name)
                except Exception as e:
                    college_name = None
                    dept_name = None
                    prerequisities = None
                    college_id = None
                    post_course_college_data(course_code, course_id, college_id, college_name, prerequisities,
                                             dept_name)
                    pass
    except Exception as e:
        print("Error raised while calling course-college table")
        pass


def post_course_college_data(course_code, course_id, college_id, college_name, prerequisities, dept_name):
    try:

        if len(college_id) > 0:
            college_id = session.query(Institution.id).where(Institution.name == college_name).first()
            Course_college_table = Course_college(course_id[0], college_id[0], prerequisities, dept_name)
            session.add(Course_college_table)
            session.commit()
            logger.info("data inserted into course-college table"), print("course-id: ", course_code)
            session.close()
        else:
            parent_university_name = yaml_obj.get(Website_URL).get('UNIVERSITY')
            insert_into_college_institution([college_name], parent_university_name)
            time.sleep(2)
            college_id = session.query(Institution.id).where(Institution.name == college_name).first()
            Course_college_table = Course_college(course_id[0], college_id[0], prerequisities, dept_name)
            session.add(Course_college_table)
            session.commit()
            logger.info("data inserted into course-college table"), print("course-id: ", course_code)
            session.close()

    except Exception as e:
        session.rollback()
        print("Error raised while inserting to post-course-college table as:", e)


def insert_into_course_gs_category(course_code, course_title, req_course_expression, general_studies):
    global course_id, gs_code_id
    logger.info("Inserting data into course_gs_category ")
    if not table_exists(engine, 'course_gs_category'):
        Base.metadata.tables['course_gs_category'].create(engine)
        logger.info("table created")
        # print("table created in database")
    try:
        for gs_code in general_studies:
            gs_code = gs_code.strip()
            # print("course title: ", course_title, ",", "GS :", gs_code)
            # print("length:", len(gs_code))
            try:
                university_name = yaml_obj.get(Website_URL).get('UNIVERSITY')
                try:
                    institution_id = session.query(Institution.id).where(Institution.name == university_name).one()
                    course_id = session.query(Course.id).where(Course.inst_id.in_(institution_id)).where(
                        Course.code == course_code).one()
                    gs_code_id = session.query(Gs_category.id).where(Gs_category.code == gs_code).first()
                except Exception as e:
                    session.rollback()
                    logger.debug("Error raised while getting mapping_id : %s" % e)
                    pass
                course_gs_category_table = Course_gs_category(course_id[0], gs_code_id[0])
                session.add(course_gs_category_table)  # persists data
                session.commit()  # commit and close session
                logger.info("data inserted into course_gs_category")
                session.close()
            except Exception as e:
                session.rollback()
                logger.debug("duplicate id found course_gs_category()")
                # print("duplicate id found course_gs_category()")
                pass
    except Exception as e:
        logger.debug("error raised in course_gs_category() %s" % e)
        # print("error raised in course_gs_category() :", e)
        pass


def insert_into_gs_category(expression, code, inst_id):
    logger.info("insert into gs_category table")
    if not table_exists(engine, 'gs_category'):
        Base.metadata.tables['gs_category'].create(engine)
        logger.info("table created")
        # print("table created in database")
    try:
        uniq_id = str(uuid.uuid4())
        external_id = hashlib.md5(str(str(inst_id[0]) + expression).encode('utf-8')).hexdigest()
        count = session.query(Gs_category.external_id).where(Gs_category.external_id == external_id).all()
        if len(count) > 0:
            logger.info("Duplicate record found")
        else:
            gs_category_table = Gs_category(uniq_id, external_id, inst_id[0], code, expression, datetime.now(),
                                            created_by[0],
                                            datetime.now(), updated_by[0])
            session.add(gs_category_table)  # persists data
            session.commit()  # commit and close session
            logger.info("data inserted into gs_category table")
            # print("gs_category data Inserted", "\n")
            session.close()
    except Exception as e:
        session.rollback()
        logger.debug("Error raised while inserting gs_category(): %s" % e)
        # print("Error raised in gs_category(): ", e)
        pass


def insert_into_requirement_variable(subject_raw_text, subject, sub_link, term_head, location, program_title):
    global requirement_id, value_id, data, uniq_id, external_id, req_external_id
    logger.info("insert into requirement-variable table")
    if not table_exists(engine, 'rqmt_variable'):
        Base.metadata.tables['rqmt_variable'].create(engine)
        logger.info("table created")
        # print("table created in database")
    try:
        # print("Requirement :", subject_raw_text, "\n")
        logger.debug("Requirement : %s" % subject_raw_text)
        driver.get(sub_link)
        time.sleep(5)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        data = extract_data_using_selector_lib(soup, "Post_curriculum_summary_1", Website_URL)
    except Exception as e:
        logger.debug("link to get soup: %s" % sub_link)
        logger.debug("Error in reqmnt-variable as no soup not found: %s" % e)
        # print("Error in reqmnt-variable as soup not found: ", e)
        sub_link = None
        subject = 'NONE'
        pass

    try:
        # --> to get requirement_id from requirement table by using external_id
        ext_group_text = term_head + program_title + convert_list_to_str(location) + subject_raw_text
        req_external_id = hashlib.md5(ext_group_text.encode('utf-8')).hexdigest()
        logger.debug("req_external_id : %s" % req_external_id)
        logger.debug("subject_raw_text: %s" % subject_raw_text)
        requirement_id = session.query(Requirement.id).where(Requirement.external_id == req_external_id).one()
    except Exception as e:
        logger.debug("no id found in (requirement_id) requirement_variable: %s" % e)
        # print("no id found in (requirement_id) requirement_variable: ", e)
        pass

    uniq_id = str(uuid.uuid4())
    ex_id = req_external_id + subject + term_head + subject_raw_text
    external_id = hashlib.md5(ex_id.encode('utf-8')).hexdigest()
    try:
        if sub_link:
            if not None in data.values():
                if len(data['course_code']) > 1:
                    try:
                        subject_text = re.split("OR | AND ", subject)
                        requirement = subject_text[0].split("(")
                        r_expression = requirement[0].strip()
                        entity = 'gs_category'
                        # gs_category_id from Gs_category
                        try:
                            value_id = session.query(Gs_category.id).where(
                                Gs_category.abbreviation == r_expression).one()
                        except Exception as e:
                            logger.debug("no id found in rqmt_variable(value_id): %s" % e)
                            pass
                            # print("no id found in (value_id)-Gs_category: ", e)
                        post_data_into_rqmt_variable(uniq_id, external_id, requirement_id[0], subject, entity,
                                                     value_id[0])
                    except Exception as e:
                        logger.debug("error raised entity :'gs_category" % e)
                        # print("error raised entity :'gs_category': ", e)
                        pass
                else:
                    try:
                        entity = 'course'
                        # course_id from Course
                        try:
                            value_id = session.query(Course.id).where(
                                Course.external_link == data['Course_title_link'][0]).first()
                        except Exception as e:
                            logger.debug("no id found for getting (value_id) in-course: %s" % e)
                            pass
                            # print("no id found in (value_id)-course: ", e)
                        post_data_into_rqmt_variable(uniq_id, external_id, requirement_id[0], subject, entity,
                                                     value_id[0])
                    except Exception as e:
                        logger.debug("error raised entity :course: %s" % e)
                        # print("error raised entity :'course': ", e)
                        pass
            else:
                try:
                    entity = 'elective'
                    value_id = None
                    post_data_into_rqmt_variable(uniq_id, external_id, requirement_id[0], subject_raw_text, entity,
                                                 value_id)
                except Exception as e:
                    logger.debug("error in requirement_variable-1:() %s" % e)
                    # print("error in requirement_variable-1:() ", e)
                    pass
        else:
            try:
                entity = 'statement'
                value_id = None
                post_data_into_rqmt_variable(uniq_id, external_id,requirement_id[0], subject_raw_text, entity, value_id)
            except Exception as e:
                logger.debug("error in requirement_variable-2:() %s" % e)
                # print("error in requirement_variable-2:() ", e)
                pass
    except Exception as e:
        session.rollback()
        logger.debug("Error raised in insert-requirement_variable(): %s" % e)
        # print("Error raised in insert-requirement_variable(): ", e)
        pass


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


def scrape_institution_website(university_name, Website_URL, inst_param_group_value, inst_param_value_level, prog_level,
                               prog_type):  # ALL programs page(HOME)
    logger.info("Stated scraping institution_website() ")
    global data

    soup = prepare_soup(Website_URL)
    seperated_soup = soup.find('tbody')
    trTags = seperated_soup.find_all('tr')

    logger.info("calling parent institution table")
    insert_into_university_institution(university_name)
    logger.info("inserting into Inst_param_value")
    master_data_into_inst_param_values(university_name)
    print("all master data insertion completed.")
    # time.sleep(120)
    try:
        for tr in trTags:
            data = extract_data_using_selector_lib(tr, "Post_course", Website_URL)
            area_title = convert_list_to_str(data['title']).strip()
            area = area_title.split(",")[0].strip()

            program_area_url = yaml_obj.get(Website_URL).get('URL') + convert_list_to_str(data['title_urls'])
            external_id = hashlib.md5(program_area_url.encode('utf-8')).hexdigest()
            check_prog_count = session.query(Program.external_id).where(Program.external_id == external_id).where(
                Program.inst_id.in_(session.query(Institution.id).where(Institution.name == university_name))).all()
            if yaml_obj.get(Website_URL).get('RESUME_SCRPAPE'):
                get_id = session.query(Program).order_by(Program.id.desc()).first()
                if get_id.external_link == program_area_url:
                    logger.debug("resumed program to scrape : %s" % area)
                    # continue
                    calling_scrape_function(data, university_name, area, inst_param_group_level, inst_param_value_level,
                                            data['degree'][0], data['title_urls'], data['location'], prog_level,
                                            prog_type)
                else:
                    # check the program before scraping
                    if len(check_prog_count) > 0:
                        logger.debug("duplicate program exist in database: %s" % area)
                    else:
                        logger.info("scraping continue")
                        logger.debug("current program to scrape : %s" % area)
                        calling_scrape_function(data, university_name, area, inst_param_group_level,
                                                inst_param_value_level,
                                                data['degree'][0], data['title_urls'], data['location'], prog_level,
                                                prog_type)
            else:
                logger.debug("ccurrent program to scrape : %s" % area)
                calling_scrape_function(data, university_name, area, inst_param_group_level, inst_param_value_level,
                                        data['degree'][0], data['title_urls'], data['location'], prog_level, prog_type)
    except Exception as e:
        print("error raised in scrape_institution_website(): ", e)


def calling_scrape_function(data, university_name, area, inst_param_group_level, inst_param_value_level, degree,
                            title_urls, location, prog_level, prog_type):
    logger.info("calling child institution table")
    inst_parent_id = insert_into_college_institution(data, university_name)

    logger.info("Inserting data into area table")

    logger.info("calling area table")
    insert_into_area(area, inst_parent_id)

    logger.info("calling degree table")
    insert_into_degree(data, inst_parent_id)

    logger.info("calling degree_level table")
    insert_into_degree_level(data, inst_param_group_level, inst_param_value_level)

    logger.info("calling location table")
    insert_into_location(data)

    # print("Data Inserted into GLobal tables")
    scrape_course_summary(degree, title_urls, area, location, inst_param_group_level,
                          prog_level, inst_parent_id, inst_param_value_level, prog_type)


# collecting program description
def scrape_course_summary(get_degree, url, area_title, program_location, inst_param_group_value, prog_level,
                          inst_parent_id, inst_param_value_level, prog_type):  # Program Description page
    logger.info("scraping course_summary()")
    try:
        program_url = yaml_obj.get(Website_URL).get('URL') + convert_list_to_str(url)
        soup = prepare_soup(program_url)
        get_program_description = soup.find('div', {'class':'mobileRow row mobile-toggle-content'})
        program_description = html_text.extract_text(f"{get_program_description}")
        insert_into_inst_location(inst_parent_id, program_location)
        data = extract_data_using_selector_lib(soup, 'Post_summary_1', Website_URL)
        insert_into_program(soup,program_url, get_degree, data, prog_level, prog_type, inst_parent_id,
                            program_location, program_description)  # prog_level, prog_type, inst_id
        program_id = insert_into_program_area(program_url, area_title)
        insert_into_program_college(program_id, data['College'])
        if yaml_obj.get(Website_URL).get('DEGREE_TYPE') == 'Masters':
            send_graduate_to_req_table(soup, program_url, data, program_id,
                                       inst_parent_id)  # related-to-graduate-programs
        get_graduate_admission_req(soup, program_url, data, program_id)
        insert_into_program_location(program_url, program_location, program_id)
        scrape_get_major_map_link(data, program_url, program_id, inst_parent_id)  # Major Map Links
    except Exception as e:
        logger.debug("Error raised while collecting course_summary as: ", e)
        # print("Error raised while collecting course_summary as:", e)
        pass


def scrape_get_major_map_link(data, program_url, program_id, inst_id):
    logger.info("collect & scrape major_map_link")
    program_title = data['Program_title'].split(",")
    # print("checking major maps")
    try:
        if data['Major_map'] is not None:  # link for on-campus classes
            logger.debug("inserting into major_map : %s" % data['Major_map'])
            major_map = data['Major_map']
            if yaml_obj.get(Website_URL).get('Requirement_type').get('required'):
                scrape_requirement_group(program_title[0].strip(), major_map, program_url,
                                         program_id)  # requirement_group
                scrape_major_map_term(major_map, inst_id)  # term
            else:
                scrape_requirement_group(program_title[0].strip(), major_map, program_url,
                                         program_id)  # requirement_group
                scrape_major_map_term_1(major_map, inst_id)

    except Exception as e:
        logger.debug("Error raise for major_map: %s" % e)
        # print("Error raise for Major_map: ", e)
        pass

    try:
        if yaml_obj.get(Website_URL).get('Major_Map_BGM').get('required'):
            data['Major_map_oncampus'] = 'https://degrees.apps.asu.edu/major-map/ASU00/TBTGMBGM/TGMBCSPC/ALL/2022'
            if data['Major_map_oncampus'] is not None:
                logger.debug("inserting into major_map oncampus : %s" % data['Major_map_oncampus'])
                major_map_oncampus = data['Major_map_oncampus']
                scrape_requirement_group(program_title[0].strip(), major_map_oncampus, program_url, program_id)
                scrape_major_map_term(major_map_oncampus, inst_id)  # term
        else:
            if data['Major_map_oncampus'] is not None:
                logger.debug("inserting into major_map oncampus : %s" % data['Major_map_oncampus'])
                major_map_oncampus = data['Major_map_oncampus']
                scrape_requirement_group(program_title[0].strip(), major_map_oncampus, program_url, program_id)
                scrape_major_map_term(major_map_oncampus, inst_id)  # term

    except Exception as e:
        logger.debug("Error raise for major_map-oncampus : %s" % e)
        # print("Error raise for Major_map_ONCAMPUS: ", e)
        pass

    try:
        if yaml_obj.get(Website_URL).get('Major_Map_BGM').get('required'):
            data['Major_map_online'] = 'https://degrees.apps.asu.edu/major-map/ASU00/TBTGMBGM/TGMBCSPC/ONLINE/2022'
            if data['Major_map_online'] is not None:
                logger.debug("inserting into major_map online : %s" % data['Major_map_online'])
                major_map_online = data['Major_map_online']
                scrape_requirement_group(program_title[0].strip(), major_map_online, program_url, program_id)
                scrape_major_map_term(major_map_online, inst_id)
        else:
            if data['Major_map_online'] is not None:
                logger.debug("inserting into major_map online : %s" % data['Major_map_online'])
                major_map_online = data['Major_map_online']
                scrape_requirement_group(program_title[0].strip(), major_map_online, program_url, program_id)
                scrape_major_map_term(major_map_online, inst_id)
    except Exception as e:
        logger.debug("Error raise for major_map-online : %s" % e)
        # print("Error raise for Major_map_ONLINE: ", e)
        pass

    try:
        if data['Major_map_concurrent'] is not None:
            logger.debug("inserting into major_map concurrent : %s" % data['Major_map_concurrent'])
            major_map_concurrent = data['Major_map_concurrent']
            scrape_requirement_group(program_title[0].strip(), major_map_concurrent, program_url, program_id)
            scrape_major_map_term(major_map_concurrent, inst_id)

    except Exception as e:
        logger.debug("Error raise for major_map-concurrent : %s" % e)
        # print("Error raise for Major_map_CONCURRENT: ", e)
        pass


def get_boolen_value(value):
    if value.upper() == 'MINIMUM':
        return True
    else:
        return False


def scrape_requirement_group(program_title, url, program_url, program_id):
    logger.info(" ")
    global Residency_hrs_minimum
    soup = prepare_soup(url)
    table_soup = soup.find_all('table', class_='termTbl')
    try:
        ex_data = extract_data_using_selector_lib(soup, "Post_curriculum_requirements_hours", Website_URL)
        try:
            Total_Hours = ex_data['Total_Hours'].split(":")
            total_credits = int(Total_Hours[1])
        except Exception as e:
            total_credits = None
        try:
            Upper_Division_Hours = ex_data['Upper_Division_Hours'].split(":")[1]
            Upper_Division_Hours = re.findall(r'\S+', Upper_Division_Hours)
            upper_dev_min = get_boolen_value(Upper_Division_Hours[1])
            upper_dev_credits = float(Upper_Division_Hours[0])
            upper_dev_credits = int(upper_dev_credits)
        except Exception as e:
            upper_dev_min = None
            upper_dev_credits = None
        try:
            Total_hrs_at_ASU = ex_data['Total_hrs_at_ASU'].split(":")[1]
            Total_hrs_at_ASU = re.findall(r'\S+', Total_hrs_at_ASU)
            tot_cred_at_prov_min = get_boolen_value(Total_hrs_at_ASU[1])
            tot_cred_at_prov = float(Total_hrs_at_ASU[0])
            tot_cred_at_prov = int(tot_cred_at_prov)
        except Exception as e:
            tot_cred_at_prov_min = None
            tot_cred_at_prov = None
        try:
            Hrs_Resident_Credit_for_Academic_Recognition = \
                ex_data['Hrs_Resident_Credit_for_Academic_Recognition'].split(":")[1]
            Hrs_Resident_Credit_for_Academic_Recognition = re.findall(r'\S+',
                                                                      Hrs_Resident_Credit_for_Academic_Recognition)
            resi_cred_min = get_boolen_value(Hrs_Resident_Credit_for_Academic_Recognition[1])
            resi_credits = float(Hrs_Resident_Credit_for_Academic_Recognition[0])
            resi_credits = int(resi_credits)
        except Exception as e:
            resi_cred_min = None
            resi_credits = None
        try:
            Total_Community_College_Hrs = ex_data['Total_Community_College_Hrs'].split(":")[1]
            Total_Community_College_Hrs = re.findall(r'\S+', Total_Community_College_Hrs)
            tot_comm_coll_cred_min = get_boolen_value(Total_Community_College_Hrs[1])
            tot_comm_coll_cred = float(Total_Community_College_Hrs[0])
            tot_comm_coll_cred = int(tot_comm_coll_cred)
        except Exception as e:
            tot_comm_coll_cred_min = None
            tot_comm_coll_cred = None
        try:
            Major_GPA = ex_data['Major_GPA'].split(":")[1]
            Major_GPA = re.findall(r'\S+', Major_GPA)
            major_gpa_min = get_boolen_value(Major_GPA[1])
            major_gpa = float(Major_GPA[0])
            major_gpa = int(major_gpa)
        except Exception as e:
            major_gpa_min = None
            major_gpa = None
        try:
            Cumulative_GPA = ex_data['Cumulative_GPA'].split(":")[1]
            Cumulative_GPA = re.findall(r'\S+', Cumulative_GPA)
            cumulative_gpa_min = get_boolen_value(Cumulative_GPA[1])
            cumulative_gpa = float(Cumulative_GPA[0])
            cumulative_gpa = int(cumulative_gpa)
        except Exception as e:
            cumulative_gpa_min = None
            cumulative_gpa = None
        try:
            insert_into_requirement_group(program_id, program_url, program_title, url, ex_data, total_credits,
                                          upper_dev_min, upper_dev_credits, tot_cred_at_prov_min, tot_cred_at_prov,
                                          resi_cred_min, resi_credits, tot_comm_coll_cred_min, tot_comm_coll_cred,
                                          major_gpa_min, major_gpa, cumulative_gpa_min, cumulative_gpa)
        except Exception as e:
            logger.debug("error in insert_into_requirement_group() : %s" % e)
            # print("error in insert_into_requirement_group() :", e)
            pass

    except Exception as e:
        logger.debug("error in scrape_requirement_group() : %s" % e)
        # print("error in scrape_requirement_group() :", e)
        pass


def scrape_major_map_term(url, inst_id):
    logger.info("scraping the term table ")
    try:
        soup = prepare_soup(url)
        data = extract_data_using_selector_lib(soup, "Post_curriculum_requirements_hours", Website_URL)
        program_title = data['Program_name']
        program_year = data['Program_year']
        location = data['Location_type']
        table_soup = soup.find_all('table', class_='termTbl')
        rqmnt_group_id = session.query(Requirement_group.id).filter(Requirement_group.external_link == url).one()
        try:
            insert_into_rqmt_group_college(rqmnt_group_id, data['College_name'])
        except Exception as e:
            print("Error raised while entering rqmt_group_college :", e)
            pass
        try:
            insert_into_rqmt_group_location(rqmnt_group_id, location)
        except Exception as e:
            print("Error raised while entering rqmt_group_location :", e)
            pass
        for each_table in table_soup:
            sub_table = each_table.find('table', class_='termTblNested')
            get_tr_tags = sub_table.find_all('tr')
            get_tr_heading_tags = each_table.find('tr', class_='termHeading')
            data_head = extract_data_using_selector_lib(get_tr_heading_tags, "Post_term_heading", Website_URL)
            term_head = convert_list_to_str(data_head['Term']).strip()
            course_hour = re.findall(r'[\d\.\d]+', convert_list_to_str(data_head['Credit_hours']))
            hours_subtotal = get_tr_tags[-1].text.strip()
            total_hours = re.findall(r'[\d\.\d]+', hours_subtotal)
            logger.info("calling term table")
            requirement_group_id = insert_into_term(url, program_year, term_head, course_hour, total_hours)

            try:
                tr_count = 0
                for each_tr in get_tr_tags:  # checking each Tr
                    try:
                        critical_course = each_tr.find('a', class_='ttCritical').img.get('alt')
                        if critical_course == 'necessary course':
                            necessary_course = True
                        else:
                            necessary_course = False

                        if critical_course == 'critical course':
                            critical_course = True
                        else:
                            critical_course = False
                    except Exception as e:
                        logger.info("No critical or necessary course found")
                        # print("No critical or necessary course found")
                        critical_course = False
                        necessary_course = False
                        pass

                    data = extract_data_using_selector_lib(each_tr, "Post_curriculum", Website_URL)
                    subject_raw_text = convert_list_to_str(data['subject_raw_text'])
                    if not convert_list_to_str(data['subject_hours']):
                        subject_hours = None
                    else:
                        subject_hours = re.findall(r'[\d\.\d]+', convert_list_to_str(data['subject_hours']))

                    if not convert_list_to_str(data['subject_minium_grade']):
                        subj_minimum_grade = None
                    else:
                        subj_minimum_grade = convert_list_to_str(data['subject_minium_grade'])

                    if None in data.values():
                        # print("Inserting into requirement table")
                        logger.info("calling requirement_1 table")
                        insert_into_requirement_1(requirement_group_id, term_head, program_title, location, url,
                                                  subject_raw_text, data["subject"], data["subject_link"],
                                                  subject_hours,
                                                  subj_minimum_grade, critical_course, necessary_course)
                        # print("Inserting into Requirement_term table")
                        logger.info("calling requirement_term table")
                        insert_into_requirement_term(requirement_group_id, url, program_title, location, term_head,
                                                     subject_raw_text)
                        try:
                            # print("Inserting into requirement_variable()")
                            logger.info("calling each requirement_variable()")

                            insert_into_requirement_variable(subject_raw_text, data["subject"], data["subject_link"],
                                                             term_head, location, program_title)
                        except Exception as e:
                            logger.debug("error in requirement_variable() :", e)
                            # print("error in requirement_variable() ")
                            pass
                    else:
                        for sub, link in zip(data['subject'], data['subject_link']):
                            logger.debug("Requirement : %s" % subject_raw_text)

                            logger.info("calling requirement table")
                            insert_into_requirement(requirement_group_id, term_head, program_title, location, url,
                                                    subject_raw_text, sub,
                                                    link, subject_hours, subj_minimum_grade, critical_course,
                                                    necessary_course)

                            # print("Inserting into Requirement_term table")
                            logger.info("calling requirement_term table")
                            insert_into_requirement_term(requirement_group_id, url, program_title, location, term_head,
                                                         subject_raw_text)

                            try:
                                # print("Inserting into course table")
                                logger.info("calling each course_curriculum")
                                scrape_course_curriculum_page(link, data["subject"], sub, inst_id)  # TABLE-7
                            except Exception as e:
                                logger.debug("No link to open #trackgroup :", e)
                                # print("No link to open #trackgroup ")
                                pass
                            try:
                                # print("Inserting into requirement_variable()")
                                logger.info("calling each requirement_variable()")

                                insert_into_requirement_variable(subject_raw_text, sub, link, term_head, location,
                                                                 program_title)
                            except Exception as e:
                                logger.debug("error in requirement_variable() :", e)
                                # print("error in requirement_variable() ")
                                pass
            except Exception as e:
                logger.debug("Error raised while collecting tr as: %s" % e)
                # print("Error raised while collecting tr as: ", e, "\n")
                pass
    except Exception as e:
        logger.info("Error raised: %s" % e)
        # print("Error raised ", e)
        pass


def scrape_major_map_term_1(url, inst_id):
    logger.info("calling the term_1 ()")
    global subject_dict, subject_raw_text, requirement_group_id
    try:
        soup = prepare_soup(url)
        data = extract_data_using_selector_lib(soup, "Post_curriculum_requirements_hours", Website_URL)
        program_title = data['Program_name']
        program_year = data['Program_year']
        location = data['Location_type']
        data = extract_data_using_selector_lib(soup, "Post_curriculum", Website_URL)
        subject_minium_grade = data['subject_minium_grade']
        logger.info("No critical or necessary course found")
        # print("No critical or necessary course found")
        # Term_table --> NULL
        critical_course = False
        necessary_course = False
        try:
            requirement_group_id = session.query(Requirement_group.id).filter(
                Requirement_group.external_link == url).one()
        except Exception as e:
            logger.debug("Error raised while getting requirement_group_id: %s" % e)
            pass
        try:
            subject_dict = {}
            for text in data['subject_raw_text']:
                subject_dict[text] = text
        except Exception as e:
            logger.debug("Error raised as: %s" % e)
            # print("Error raised subject_dict{} as:", e)
            pass

        try:
            subject_raw_text = []
            for subj in data['subject']:
                for key in subject_dict.keys():
                    if subj in key:
                        subject_raw_text.append(key)
        except Exception as e:
            logger.debug("Error raised as: %s" % e)
            # print("Error raised subject_raw_text[] as:", e)
            pass

        for sub_raw, subject, link in zip(subject_raw_text, data['subject'], data['subject_link']):
            try:
                sub_hour = re.findall('[0-9]+', sub_raw)
                hour = [sub_hour[-1]]
                logger.info("calling requirement (term_1) table")
                # print(sub_raw,",", subject,",", link, "\n")
                term_head = 'map'  # to generate in original_id
                insert_into_requirement(requirement_group_id, term_head, program_title, location, url, sub_raw, subject,
                                        link, hour, subject_minium_grade, critical_course, necessary_course)
                try:
                    # print("Inserting into course table")
                    logger.info("calling each course_curriculum")
                    scrape_course_curriculum_page(link, [sub_raw], subject, inst_id)  # TABLE-7
                except Exception as e:
                    logger.debug("No link to open in requirement :", e)
                    # print("No link to open #trackgroup ")
                    pass
                try:
                    # print("Inserting into requirement_variable()")
                    logger.info("calling each requirement_variable() in term_1")
                    insert_into_requirement_variable(sub_raw, subject, link, term_head, location, program_title)
                except Exception as e:
                    logger.debug("error in requirement_variable() :", e)
                    # print("error in requirement_variable() ")
                    pass
            except Exception as e:
                logger.debug("Error in term_requirement loop as: %s" % e)
                # print("Error in term_ requirement loop as:", e)
                pass

    except Exception as e:
        logger.debug("Error raised in scrape_major_map_term_1(): %s" % e)
        # print("Error raised in scrape_major_map_term_1():", e)
        pass


def scrape_course_curriculum_page(link, subject_text, subject, inst_id):  # Course_catalog Page
    # print("scraping requirement: ", subject, ",,", "course scraping url: ", link)
    try:
        global r_expression, soup, r_code
        try:
            driver.get(link)
            time.sleep(4)
            soup = BeautifulSoup(driver.page_source, 'html.parser')
        except Exception as e:
            logger.debug("Error while collecting soup in scrape_course_curriculum_page(): %s" % e)

        data = extract_data_using_selector_lib(soup, "Post_curriculum_summary_1", Website_URL)
        logger.debug("current requirement: %s" % subject)
        logger.debug("scraping url: %s" % link)
        if len(data['course_code']) > 1:
            try:
                requirement = subject.split("(")
                r_expression = requirement[0].strip()
                r_code = requirement[1].split(")")
                r_code = r_code[0].strip()  # "In gs_category code should not be number"
                if r_code.isdigit():
                    r_code = None
                    show_course_next_page(link, r_expression, inst_id)
                else:
                    # to map the requirement_text with Gs_code in course table into gs_category
                    insert_into_gs_category(r_expression, r_code, inst_id)
                    logger.info("calling pagination function")
                    logger.debug("current pagiantion for: %s" % r_expression)

                    try:
                        if subject not in check_subject_pagination:
                            check_subject_pagination.append(subject)
                            logger.debug("check_pagination req subject: %s" % check_subject_pagination)
                            show_course_next_page(link, r_expression, inst_id)
                        else:
                            # print("pagination for this subject already scrapped: %s", subject)
                            logger.debug("pagination for this subject already scrapped: %s" % subject)
                    except Exception as e:
                        logger.debug(" Error as: %s" % e)
                        # print(" Error as: ", e)
            except Exception as e:
                logger.debug(" Error raised for gs_category %s" % e)
                # print(" Error raised for gs_category", e)
                pass
        else:
            try:
                gs_subject = soup.find(class_='gstip_course').attrs['href']
                r_expression = re.sub("[|]", '', gs_subject)
                # print("expresion :", r_expression)
                r_code = soup.find(class_='gstip_course').text
                get_code = re.sub("[(,)]", '', r_code)
                r_code = get_code.strip()
                # print("code :", r_code)
            except Exception as e:
                r_expression = None
                pass
            if r_expression is None:
                # print("no general studies found for ", subject)
                logger.debug("no general studies found for %s" % subject)
                logger.info("calling insert_into_course() ")
                course_code = data['course_code'][0].strip()
                logger.debug("course code: %s " % course_code)
                count = session.query(Course.code).where(Course.code == course_code).all()
                if len(count) > 0:
                    logger.info("duplicate record found in course table")
                    # print("duplicate record found in course table")
                else:
                    for course_code, title, title_link, desciption, course_credit, gs in zip(data['course_code'],
                                 data['Course_title'], data['Course_title_link'], data['course_description'],
                                 data['Course_credits'], data['Course_gs']):
                        # print("calling course table", "\n")
                        try:
                            insert_into_course(soup, link, course_code, title, title_link, desciption, course_credit,
                                               gs, r_expression, inst_id)
                        except Exception as e:
                            # print("Error while calling course table-0")
                            pass
                        try:
                            insert_into_course_college(course_code, data)
                        except Exception as e:
                            print("Error while calling course college-1")
                            pass

            else:
                logger.info("inserting into Gs_category")
                count = session.query(Gs_category.code).where(Gs_category.code == r_code).all()
                if len(count) > 0:
                    # print("duplicate record in Gs-category")
                    logger.info("duplicate record in Gs-category")
                else:
                    logger.info("calling & inserting into Gs-category")
                    insert_into_gs_category(r_expression, r_code, inst_id)
                logger.info("calling course table")
                course_code = data['course_code'][0].strip()
                logger.debug("course code: %s " % course_code)
                count = session.query(Course.code).where(Course.code == course_code).all()
                if len(count) > 0:
                    logger.info("duplicate record found in course table")
                    # print("duplicate record found in course table")
                else:
                    try:
                        logger.info("calling insert_into_course() ")
                        for course_code, title, title_link, desciption, course_credit, gs in zip(data['course_code'],
                                 data['Course_title'],data['Course_title_link'], data['course_description'],
                                 data['Course_credits'],data['Course_gs']):
                            # print("calling course table", "\n")
                            try:
                                logger.info("calling & inserting course table")
                                insert_into_course(soup, link, course_code, title, title_link, desciption,
                                                   course_credit, gs, r_expression, inst_id)
                            except Exception as e:
                                # print("Error while calling course table-1")
                                logger.debug("Error while inserting into course table-1: %s" % e)
                                pass
                            try:
                                insert_into_course_college(course_code, data)
                            except Exception as e:
                                print("Error while calling course college-0")
                                pass

                    except Exception as e:
                        logger.debug("Error raised while insert_into_course() : %s" % e)
                        pass
    except Exception as e:
        logger.debug("Error raised when No pages found -scrape_course_curriculum_page() : %s" % e)
        pass


def show_course_next_page(url, expression, inst_id):
    try:
        logger.info("searching page numbers in course page")
        # print("scraping requirement: ", expression, ",,", "pagination scraping url: ", url)
        logger.debug("pagination scraping url: %s" % url)
        logging.debug("scraping requirement: %s" % expression)
        driver.get(url)
        time.sleep(3)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        data = extract_data_using_selector_lib(soup, "Post_curriculum_summary_1", Website_URL)
        get_gs_expression = soup.find_all(class_='gstip_course')
        for each_gs in get_gs_expression:
            try:
                gs_subject = each_gs['href']
                get_expression = re.sub("[|]", '', gs_subject)
                # print("expresion :", get_expression)
                get_code = each_gs.text
                get_code = re.sub("[(,)]", '', get_code)
                get_code = get_code.strip()
                # print("code :", get_code)
                logger.info("calling Gs_categories")
                count = session.query(Gs_category.code).where(Gs_category.code == get_code).all()
                if len(count) > 0:
                    # print("duplicate record in Gs-category")
                    logger.info("duplicate record in Gs-category")
                else:
                    logger.info("calling & inserting into Gs-category")
                    insert_into_gs_category(get_expression, get_code, inst_id)
            except Exception as e:
                get_expression = None
                logger.debug("No more General-studies to insert: %s" % e)
                pass
        try:
            logger.info("iterating data for pagination-1")
            print("available course in first-page is :", len(data['course_code']))
            for course_code, title, title_link, desciption, course_credit, gs in zip(data['course_code'],
                              data['Course_title'],data['Course_title_link'],data['course_description'],data['Course_credits'],
                              data['Course_gs']):
                # print("calling course table", "\n")
                try:
                    course_code = course_code.strip()
                    count = session.query(Course.code).where(Course.code == course_code).all()

                    if len(count) > 0:
                        logger.info("duplicate record found in course table")
                        # print("duplicate record found in course table")
                    else:
                        logger.info("calling & inserting course table")
                        insert_into_course(soup, url, course_code, title, title_link, desciption, course_credit, gs,
                                           expression, inst_id)
                        try:
                            calling_insert_into_course_college(course_code)
                        except Exception as e:
                            print("Error raised while calling_insert_into_course_college()-1", e)

                except Exception as e:
                    logger.debug("Error raised while inserting courses for pagination-1: %s" % e)
                    # print("Error while calling course table for pagination-1")
                    pass
        except Exception as e:
            logger.debug("Error raised while calling course table for pagination-1: %s" % e)
            pass
        logger.info("checking & finding the pagination")
        if yaml_obj.get(Website_URL).get('Pagination').get('required'):
            page_numbers = extract_data_using_selector_lib(soup, "Pagination_urls", Website_URL)
            # print("pages found: %s", page_numbers['Urls'])
            logger.debug("pages found: %s" % page_numbers['Urls'])
            count = 1
            # general_studies = ''
            logger.info("pagination scraping complete for page: 1")
            if len(page_numbers['Urls']) > 3:
                while count < (int(len(page_numbers['Urls'])) - 2):
                    if yaml_obj.get(Website_URL).get('Click_next_button').get('required'):
                        time.sleep(2)
                        try:
                            count += 1
                            logger.debug("next page number: %s" % count)
                            print("next_page count :", count)
                            if driver.find_element(By.XPATH,yaml_obj.get(Website_URL).get('Click_next_button').get('Xpath')):
                                time.sleep(3)
                                driver.find_element(By.XPATH, yaml_obj.get(Website_URL).get('Click_next_button').get('Xpath')).click()
                                time.sleep(2)
                                soup = BeautifulSoup(driver.page_source, 'html.parser')
                                logger.debug("collecting data for page: %s" % count)
                                data = extract_data_using_selector_lib(soup, "Post_curriculum_summary_1", Website_URL)
                                print("total courses collected on page- ", count, " is :", len(data['course_code']),"\n")
                                try:
                                    for course_code, title, title_link, desciption, course_credit, gs in zip(
                                            data['course_code'], data['Course_title'], data['Course_title_link'],
                                            data['course_description'], data['Course_credits'], data['Course_gs']):

                                        print("calling course table to insert-- ", course_code)

                                        try:
                                            course_code = course_code.strip()
                                            time.sleep(2)
                                            get_count = session.query(Course.code).where(Course.code == course_code).all()
                                            if len(get_count) > 0:
                                                logger.info("duplicate record found in course table: %s" % course_code)
                                                # print("duplicate record found in course table")
                                            else:
                                                logger.info("calling & inserting course table")
                                                insert_into_course(soup, url, course_code, title, title_link,
                                                                   desciption, course_credit, gs, expression, inst_id)
                                                try:
                                                    calling_insert_into_course_college(course_code)
                                                except Exception as e:
                                                    print("Error raised while calling_insert_into_course_college()-2",e)

                                        except Exception as e:
                                            logger.debug("Error while calling inserting records : %s" % e)
                                            # print("Error while calling inserting records : %s" % e)
                                            pass

                                    logger.debug("completed pagination for page: %s" % count)
                                    print("completed pagination for page: " ,count)
                                except Exception as e:
                                    logger.debug("Error raised while inserting courses for pagination : %s" % e)
                                    pass
                        except Exception as e:
                            logger.debug("Getting Error while collecting pagination:  %s" % e)
                            pass
            logger.info("No more pages to scrape")
    except Exception as e:
        logger.debug("Error raised for show_course_next_page :%s" % e)
        pass


if __name__ == '__main__':
    logger.info("work site: Arizona State University")

    ASU_Website_URL = [
        ##### Undergraduate programs ####
        # "https://degrees.apps.asu.edu/bachelors/major-list/keyword/Jewish%20Studies",
        # "https://degrees.apps.asu.edu/bachelors/major-list/keyword/BGM",
        # "https://degrees.apps.asu.edu/bachelors/major-list/keyword/Actuarial%20Science",

        #### ALL are graduate programs  ######
        # "https://degrees.apps.asu.edu/masters-phd/major-list/keyword/Geography,%20MA"
        # "https://degrees.apps.asu.edu/masters-phd/major-list/keyword/%20Actuarial%20Science,%20MS"
        # "https://degrees.apps.asu.edu/masters-phd/major-list/keyword/Digital%20Audience%20Strategy,%20MS",
        # "https://degrees.apps.asu.edu/masters-phd/major-list/keyword/MPM",
        "https://degrees.apps.asu.edu/masters-phd/major-list/keyword/Engineering%20Science%20(Software%20Engineering),%20MSE"
    ]

    for Website_URL in ASU_Website_URL:
        logger.debug("scraping website: %s" % Website_URL)
        soup = prepare_soup(Website_URL)
        university_name = yaml_obj.get(Website_URL).get('UNIVERSITY')
        inst_param_group_level = yaml_obj.get(Website_URL).get('INST_PARAM_GROUP_LEVEL')
        inst_param_value_level = yaml_obj.get(Website_URL).get('INST_PARAM_VALUE_LEVEL')
        prog_level = yaml_obj.get(Website_URL).get('PROGRAM_LEVEL')  # 'PROGRAM_LEVEL'
        prog_type = yaml_obj.get(Website_URL).get('PROGRAM_TYPE')  # '%Undergraduate%'
        try:
            print("scraping_started for:", Website_URL)
            logger.debug("scraping started for : %s" % Website_URL)
            # check the boolean for START_SCRAPE in selector.yaml
            if yaml_obj.get(Website_URL).get('START_SCRAPE'):
                scrape_institution_website(university_name, Website_URL, inst_param_group_level, inst_param_value_level,
                                           prog_level, prog_type)
                logger.debug("scraping completed for : %s" % Website_URL)
                print("scraping completed for!!:", Website_URL)
            else:
                print("here START_SCRAPE is false ")
                scrape_institution_website(university_name, Website_URL, inst_param_group_level, inst_param_value_level,
                                           prog_level, prog_type)
                print("!!scraping completed for:", Website_URL)
                logger.debug("scraping completed for : %s" % Website_URL)
        except Exception as e:
            logger.debug("Error found in __main()__ %s" % e)
    driver.close()
    driver.quit()
    logger.error(" Exception while quit driver ")
    logger.info("Driver closed")
