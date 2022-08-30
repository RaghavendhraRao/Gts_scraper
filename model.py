from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.mysql import LONGTEXT, ENUM
from sqlalchemy import Column, DateTime, BigInteger, CHAR, VARCHAR, UniqueConstraint, String, ForeignKey, Table, INT, \
    Sequence, MetaData, BINARY, VARBINARY, Float
from sqlalchemy.dialects.mysql import TINYINT as Tinyint
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy import Index
import datetime

Base = declarative_base()
metadata = MetaData()


class User(Base):
    # CREATE TABLE `user` (
    #   `uuid` varchar(75) DEFAULT NULL,
    #   `id` bigint(20) NOT NULL,
    #   `first_name` VARCHAR(75) DEFAULT NULL,
    #   `middle_name` VARCHAR(75) DEFAULT NULL,
    #   `last_name` VARCHAR(75) DEFAULT NULL,
    #   `email` VARCHAR(75) DEFAULT NULL,
    #   `password` VARCHAR(75) DEFAULT NULL,
    #   `language_id` VARCHAR(75) DEFAULT NULL,
    #   `timezone_id` VARCHAR(75) DEFAULT NULL,
    #   `created_at` datetime DEFAULT NULL,
    #   `created_by` bigint(20) DEFAULT NULL,
    #   `updated_at` datetime DEFAULT NULL,
    #   `updated_by` bigint(20) DEFAULT NULL,
    #   `active` tinyint(1) DEFAULT NULL,
    #   PRIMARY KEY (`id`),
    #   KEY `user_created_by` (`created_by`),
    #   KEY `user_updated_by` (`updated_by`),
    #   CONSTRAINT `user_created_by` FOREIGN KEY (`created_by`) REFERENCES `user` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
    #   CONSTRAINT `user_updated_by` FOREIGN KEY (`updated_by`) REFERENCES `user` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
    # ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    __tablename__ = 'user'
    uuid = Column('uuid', VARCHAR(75), unique=True, nullable=True, default=None)
    external_id = Column('external_id', VARCHAR(75), unique=True, nullable=True)
    user_seq = Sequence('user_seq' ,increment=1)
    id = Column('id', BigInteger, user_seq, primary_key=True)
    # id = Column('id', BigInteger, primary_key=True, autoincrement=True, default=None)
    first_name = Column('first_name', VARCHAR(75, collation='utf8mb4_unicode_ci'), nullable=True, default=None)
    middle_name = Column('middle_name', VARCHAR(75, collation='utf8mb4_unicode_ci'), nullable=True, default=None)
    last_name = Column('last_name', VARCHAR(75, collation='utf8mb4_unicode_ci'), nullable=True, default=None)
    email = Column('email', VARCHAR(75, collation='utf8mb4_unicode_ci'), nullable=True, default=None)
    password = Column('password', VARCHAR(75, collation='utf8mb4_unicode_ci'), nullable=True, default=None)
    language_id = Column('language_id', VARCHAR(75, collation='utf8mb4_unicode_ci'), nullable=True, default=None)
    timezone_id = Column('timezone_id', VARCHAR(75, collation='utf8mb4_unicode_ci'), nullable=True, default=None)
    created_at = Column('created_at', DateTime, nullable=True, default=None)
    created_by = Column('created_by', BigInteger, ForeignKey("user.id"))
    updated_at = Column('updated_at', DateTime, nullable=True, default=None)
    updated_by = Column('updated_by', BigInteger, ForeignKey("user.id"))
    active = Column('active', Tinyint, nullable=True, default=1)

    def __init__(self, uuid,external_id, first_name, middle_name, last_name, email, password, language_id, timezone_id, created_at,
                 created_by, updated_at, updated_by):
        self.uuid = uuid
        self.external_id = external_id
        self.first_name = first_name
        self.middle_name = middle_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.language_id = language_id
        self.timezone_id = timezone_id
        self.created_at = created_at
        self.created_by = created_by
        self.updated_at = updated_at
        self.updated_by = updated_by


class Inst_param_group(Base):
    # CREATE TABLE `inst_parm_group` (
    #   `id` bigint(20) NOT NULL,
    #   `name` VARCHAR(75) DEFAULT NULL,
    #   `description` varchar(200) DEFAULT NULL,
    #   `active` tinyint(1) DEFAULT NULL,
    #   PRIMARY KEY (`id`)
    # ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    __tablename__ = 'inst_param_group'
    # id = Column('id', BigInteger, primary_key=True, nullable=True)
    INST_PARAM_GROUP_seq = Sequence('INST_PARAM_GROUP_seq' ,increment=1)
    id = Column('id', BigInteger, INST_PARAM_GROUP_seq, primary_key=True)
    name = Column('name', VARCHAR(75, collation='utf8mb4_unicode_ci'), nullable=True, default=None)
    description = Column('description', VARCHAR(200, collation='utf8mb4_unicode_ci'), nullable=True, default=None)
    active = Column('active', Tinyint, nullable=True)

    def __init__(self,id,name, description, active):
        self.id = id
        self.name = name
        self.description = description
        self.active = active


class Inst_param_value(Base):
    # CREATE TABLE `inst_param_value` (
    #   `id` bigint(20) NOT NULL,
    #   `inst_param_group_id` bigint(20) DEFAULT NULL,
    #   `inst_id` bigint(20) DEFAULT NULL,
    #   `name` VARCHAR(75) DEFAULT NULL,
    #   `description` VARCHAR(75) DEFAULT NULL,
    #   `editable` tinyint(4) DEFAULT NULL,
    #   `active` tinyint(1) DEFAULT NULL,
    #   PRIMARY KEY (`id`),
    #   KEY `inst_param_value_inst_param_group_id_idx` (`inst_param_group_id`),
    #   KEY `inst_param_value_institution_id_idx` (`inst_id`),
    #   CONSTRAINT `inst_param_value_inst_param_group_id` FOREIGN KEY (`inst_param_group_id`) REFERENCES `inst_parm_group` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
    #   CONSTRAINT `inst_param_value_institution_id` FOREIGN KEY (`inst_id`) REFERENCES `institution` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
    # ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

    __tablename__ = 'inst_param_value'
    # id = Column('id', BigInteger, primary_key=True, nullable=True)
    inst_param_value_seq = Sequence('inst_param_value_seq',increment=1)
    id = Column('id', BigInteger, inst_param_value_seq, primary_key=True)
    inst_param_group_id = Column('inst_param_group_id', BigInteger, nullable=True)
    inst_id = Column(BigInteger, ForeignKey("institution.id"))
    name = Column('name', VARCHAR(75, collation='utf8mb4_unicode_ci'), nullable=True, default=None)
    description = Column('description', VARCHAR(255, collation='utf8mb4_unicode_ci'), nullable=True, default=None)
    editable = Column('editable', Tinyint, nullable=True, default=1)
    active = Column('active', Tinyint, nullable=True)

    def __init__(self, inst_param_group_id, inst_id, name, description, editable, active):
        # self.id = id
        self.inst_param_group_id = inst_param_group_id
        self.inst_id = inst_id
        self.name = name
        self.description = description
        self.editable = editable
        self.active = active


class App_param_group(Base):
    # CREATE TABLE `app_param_group` (
    #   `id` bigint(20) NOT NULL AUTO_INCREMENT,
    #   `name` varchar(75) DEFAULT NULL,
    #   `description` varchar(150) DEFAULT NULL,
    #   `active` tinyint(1) DEFAULT NULL,
    #   PRIMARY KEY (`id`)
    # ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

    __tablename__ = 'app_param_group'
    # id = Column('id', BigInteger, primary_key=True, nullable=True)
    APP_PARAM_GROUP_seq = Sequence('APP_PARAM_GROUP_seq' ,increment=1)
    id = Column('id', BigInteger, APP_PARAM_GROUP_seq, primary_key=True)
    name = Column('name', VARCHAR(75, collation='utf8mb4_unicode_ci'), nullable=True, default=None)
    description = Column('description', VARCHAR(255, collation='utf8mb4_unicode_ci'), nullable=True, default=None)
    active = Column('active', Tinyint, nullable=True)

    def __init__(self,id, name, description, active):
        self.id = id
        self.name = name
        self.description = description
        self.active = active


class App_param_value(Base):
    # CREATE TABLE `app_param_value` (
    #   `id` bigint(20) NOT NULL AUTO_INCREMENT,
    #   `app_param_group_id` bigint(20) DEFAULT NULL,
    #   `name` varchar(75) DEFAULT NULL,
    #   `description` varchar(150) DEFAULT NULL,
    #   `editable` tinyint(4) DEFAULT NULL,
    #   `active` tinyint(1) DEFAULT NULL,
    #   PRIMARY KEY (`id`),
    #   UNIQUE KEY `definition_valuecol_UNIQUE` (`description`),
    #   KEY `definition_value_definition_group_id_idx` (`app_param_group_id`),
    #   CONSTRAINT `app_param_value_app_param_group_id` FOREIGN KEY (`app_param_group_id`) REFERENCES `app_param_group` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
    # ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

    __tablename__ = 'app_param_value'
    APP_PARAM_VALUE_seq = Sequence('APP_PARAM_VALUE_seq', increment=1)
    id = Column('id', BigInteger, APP_PARAM_VALUE_seq, primary_key=True)
    app_param_group_id = Column(BigInteger, ForeignKey("app_param_group.id"))
    name = Column('name', VARCHAR(75, collation='utf8mb4_unicode_ci'), nullable=True, default=None)
    description = Column('description', VARCHAR(255, collation='utf8mb4_unicode_ci'), nullable=True, default=None)
    editable = Column('editable', Tinyint, nullable=True, default=1)
    active = Column('active', Tinyint, nullable=True)

    def __init__(self,id, app_param_group_id, name, description, editable, active):
        self.id = id
        self.app_param_group_id = app_param_group_id
        self.name = name
        self.description = description
        self.editable = editable
        self.active = active


class Country(Base):
    # CREATE TABLE `country` (
    #   `id` bigint(20) NOT NULL,
    #   `name` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
    #   `code` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
    #   `active` tinyint(4) DEFAULT NULL,
    #   PRIMARY KEY (`id`)
    # ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

    __tablename__ = 'country'
    country_seq = Sequence('country_seq', increment=1, )
    id = Column('id', BigInteger, country_seq, primary_key=True)
    name = Column('name', VARCHAR(255, collation='utf8mb4_unicode_ci'), nullable=True, default=None)
    code = Column('code', VARCHAR(75, collation='utf8mb4_unicode_ci'), nullable=True, default=None)
    active = Column('active', Tinyint, nullable=True, default=1)

    def __init__(self, name, code):
        self.name = name
        self.code = code


class Institution(Base):
    # `uuid` varchar(75) DEFAULT NULL,
    #   `id` bigint(20) NOT NULL,
    #   `name` VARCHAR(75) DEFAULT NULL,
    #   `code` VARCHAR(75) DEFAULT NULL,
    #   `type` VARCHAR(75) DEFAULT NULL,
    #   `parent_id` bigint(20) DEFAULT NULL,
    #   `created_at` datetime DEFAULT NULL,
    #   `created_by` bigint(20) DEFAULT NULL,
    #   `updated_at` datetime DEFAULT NULL,
    #   `updated_by` bigint(20) DEFAULT NULL,
    #   `active` tinyint(1) DEFAULT NULL,
    #   PRIMARY KEY (`id`),
    #   KEY `institution_created_by_idx` (`created_by`),
    #   KEY `institution_updated_by_idx` (`updated_by`),
    #   CONSTRAINT `FK5liqjwfiuove11aqb5wn8tamj` FOREIGN KEY (`updated_by`) REFERENCES `user` (`id`),
    #   CONSTRAINT `FK8hestroj5c6d48bdwj5jcg41c` FOREIGN KEY (`created_by`) REFERENCES `user` (`id`),
    #   CONSTRAINT `institution_created_by` FOREIGN KEY (`created_by`) REFERENCES `user` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
    #   CONSTRAINT `institution_updated_by` FOREIGN KEY (`updated_by`) REFERENCES `user` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
    # ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

    __tablename__ = 'institution'
    uuid = Column('uuid', VARCHAR(75), unique=True, nullable=True)
    # id = Column('id', BigInteger, primary_key=True, autoincrement=True)
    institution_seq = Sequence('institution_seq' ,increment=1, )
    id = Column('id', BigInteger, institution_seq, primary_key=True)
    external_id = Column('external_id', VARCHAR(75), unique=True, nullable=True)
    name = Column('name', VARCHAR(75, collation='utf8mb4_unicode_ci'), nullable=True, default=None)
    code = Column('code', VARCHAR(75, collation='utf8mb4_unicode_ci'), nullable=True, default=None)
    country_id = Column('country_id', BigInteger, ForeignKey("country.id"))
    type = Column('type', VARCHAR(75, collation='utf8mb4_unicode_ci'), nullable=True, default=None)
    parent_id = Column(BigInteger, ForeignKey("institution.id"))
    created_at = Column('created_at', DateTime, nullable=True)
    created_by = Column('created_by', BigInteger, ForeignKey("user.id"))
    updated_at = Column('updated_at', DateTime, nullable=True)
    updated_by = Column('updated_by', BigInteger, ForeignKey("user.id"))
    active = Column('active', Tinyint, nullable=True, default=1)

    def __init__(self, uuid, external_id, name, code,country_id, type, parent_id, created_at, created_by, updated_at, updated_by):
        self.uuid = uuid
        self.external_id = external_id
        self.name = name
        self.code = code
        self.country_id = country_id
        self.type = type
        self.parent_id = parent_id
        self.created_at = created_at
        self.created_by = created_by
        self.updated_at = updated_at
        self.updated_by = updated_by
        # self.active = active


class Institution_location(Base):
    # CREATE TABLE `institution_location` (
    #   `inst_id` bigint(20) NOT NULL,
    #   `location_id` bigint(20) NOT NULL,
    #   PRIMARY KEY (`inst_id`,`location_id`),
    #   KEY `institution_location_institution_id_idx` (`inst_id`),
    #   KEY `institution_location_location_id_idx` (`location_id`),
    #   CONSTRAINT `institution_location_institution_id` FOREIGN KEY (`inst_id`) REFERENCES `institution` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
    #   CONSTRAINT `institution_location_location_id` FOREIGN KEY (`location_id`) REFERENCES `location` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
    # ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    __tablename__ = 'institution_location'
    inst_id = Column("inst_id", BigInteger, ForeignKey("institution.id"), primary_key=True)
    location_id = Column("location_id", BigInteger, ForeignKey("location.id"), primary_key=True)

    def __init__(self, inst_id, location_id):
        self.inst_id = inst_id
        self.location_id = location_id


class Area(Base):
    # CREATE TABLE `area` (
    #   `uuid` varchar(75) DEFAULT NULL,
    #   `id` bigint(20) NOT NULL,
    #   `name` VARCHAR(75) DEFAULT NULL,
    #   `inst_id` bigint(20) DEFAULT NULL,
    #   `created_at` datetime DEFAULT NULL,
    #   `created_by` bigint(20) DEFAULT NULL,
    #   `updated_at` datetime DEFAULT NULL,
    #   `updated_by` bigint(20) DEFAULT NULL,
    #   `active` tinyint(1) DEFAULT NULL,
    #   PRIMARY KEY (`id`),
    #   KEY `area_institution_id_idx` (`inst_id`),
    #   KEY `area_created_by_idx` (`created_by`),
    #   KEY `area_updated_by_idx` (`updated_by`),
    #   CONSTRAINT `area_created_by` FOREIGN KEY (`created_by`) REFERENCES `user` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
    #   CONSTRAINT `area_institution_id` FOREIGN KEY (`inst_id`) REFERENCES `institution` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
    #   CONSTRAINT `area_updated_by` FOREIGN KEY (`updated_by`) REFERENCES `user` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
    # ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

    __tablename__ = 'area'
    uuid = Column('uuid', VARCHAR(75), unique=True, nullable=True)
    # id = Column('id', BigInteger, primary_key=True, autoincrement=True)
    area_seq = Sequence('area_seq' ,increment=1)
    id = Column('id', BigInteger, area_seq, primary_key=True)
    external_id = Column('external_id', VARCHAR(75), unique=True, nullable=True)
    name = Column('name', VARCHAR(75, collation='utf8mb4_unicode_ci'), nullable=True, default=None)
    inst_id = Column(BigInteger, ForeignKey("institution.id"))
    created_at = Column('created_at', DateTime, nullable=True)
    created_by = Column('created_by', BigInteger, ForeignKey("user.id"))
    updated_at = Column('updated_at', DateTime, nullable=True)
    updated_by = Column('updated_by', BigInteger, ForeignKey("user.id"))
    active = Column('active', Tinyint, nullable=True, default=1)

    def __init__(self, uuid, external_id, name, inst_id, created_at, created_by, updated_at, updated_by):
        self.uuid = uuid
        self.external_id = external_id
        self.name = name
        self.inst_id = inst_id
        self.created_at = created_at
        self.created_by = created_by
        self.updated_at = updated_at
        self.updated_by = updated_by


class Degree(Base):
    # CREATE TABLE `degree` (
    #   `uuid` varchar(75) DEFAULT NULL,
    #   `id` bigint(20) NOT NULL,
    #   `name` VARCHAR(75) DEFAULT NULL,
    #   `inst_id` bigint(20) DEFAULT NULL,
    #   `created_at` datetime DEFAULT NULL,
    #   `created_by` bigint(20) DEFAULT NULL,
    #   `updated_at` datetime DEFAULT NULL,
    #   `updated_by` bigint(20) DEFAULT NULL,
    #   `active` tinyint(1) DEFAULT NULL,
    #   PRIMARY KEY (`id`),
    #   KEY `degree_institution_id_idx` (`inst_id`),
    #   CONSTRAINT `degree_institution_id` FOREIGN KEY (`inst_id`) REFERENCES `institution` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
    # ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

    __tablename__ = 'degree'
    uuid = Column('uuid', VARCHAR(75), unique=True, nullable=True)
    # id = Column('id', BigInteger, primary_key=True, autoincrement=True)
    degree_seq = Sequence('degree_seq' ,increment=1)
    id = Column('id', BigInteger, degree_seq, primary_key=True)
    external_id = Column('external_id', VARCHAR(75), unique=True, nullable=True)
    name = Column('name', VARCHAR(75, collation='utf8mb4_unicode_ci'), nullable=True, default=None)
    inst_id = Column(BigInteger, ForeignKey("institution.id"))
    created_at = Column('created_at', DateTime, nullable=True)
    created_by = Column('created_by', BigInteger, ForeignKey("user.id"))
    updated_at = Column('updated_at', DateTime, nullable=True)
    updated_by = Column('updated_by', BigInteger, ForeignKey("user.id"))
    active = Column('active', Tinyint, nullable=True, default=1)

    def __init__(self, uuid, external_id, name, inst_id, created_at, created_by, updated_at, updated_by):
        self.uuid = uuid
        self.external_id = external_id
        self.name = name
        self.inst_id = inst_id
        self.created_at = created_at
        self.created_by = created_by
        self.updated_at = updated_at
        self.updated_by = updated_by


class Location(Base):
    # CREATE TABLE `location` (
    #   `uuid` varchar(75) DEFAULT NULL,
    #   `id` bigint(20) NOT NULL,
    #   `inst_id` bigint(20) DEFAULT NULL,
    #   `name` VARCHAR(75) DEFAULT NULL,
    #   `code` VARCHAR(75) DEFAULT NULL,
    #   `created_at` datetime DEFAULT NULL,
    #   `created_by` bigint(20) DEFAULT NULL,
    #   `updated_at` datetime DEFAULT NULL,
    #   `updated_by` bigint(20) DEFAULT NULL,
    #   `active` tinyint(1) DEFAULT NULL,
    #   PRIMARY KEY (`id`),
    #   KEY `location_institution_id_idx` (`inst_id`),
    #   KEY `location_created_by_idx` (`created_by`),
    #   KEY `location_updated_by_idx` (`updated_by`),
    #   CONSTRAINT `location_created_by` FOREIGN KEY (`created_by`) REFERENCES `user` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
    #   CONSTRAINT `location_institution_id` FOREIGN KEY (`inst_id`) REFERENCES `institution` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
    #   CONSTRAINT `location_updated_by` FOREIGN KEY (`updated_by`) REFERENCES `user` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
    # ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

    __tablename__ = 'location'
    uuid = Column('uuid', VARCHAR(75), unique=True, nullable=True)
    # id = Column('id', BigInteger, primary_key=True, autoincrement=True)
    location_seq = Sequence('location_seq',increment=1)
    id = Column('id', BigInteger, location_seq, primary_key=True)
    external_id = Column('external_id', VARCHAR(75), unique=True, nullable=True)
    name = Column('name', VARCHAR(75, collation='utf8mb4_unicode_ci'), nullable=True, default=None)
    code = Column('code', VARCHAR(75, collation='utf8mb4_unicode_ci'), nullable=True, default=None)
    created_at = Column('created_at', DateTime, nullable=True)
    created_by = Column('created_by', BigInteger, ForeignKey("user.id"))
    updated_at = Column('updated_at', DateTime, nullable=True)
    updated_by = Column('updated_by', BigInteger, ForeignKey("user.id"))
    active = Column('active', Tinyint, nullable=True, default=1)

    def __init__(self, uuid, external_id, name, code, created_at, created_by, updated_at, updated_by):
        self.uuid = uuid
        self.external_id = external_id
        self.name = name
        self.code = code
        self.created_at = created_at
        self.created_by = created_by
        self.updated_at = updated_at
        self.updated_by = updated_by


class Degree_level(Base):
    # CREATE TABLE `degree_level` (
    #   `id` bigint(20) NOT NULL,
    #   `degree_id` bigint(20) DEFAULT NULL,
    #   `level_id` bigint(20) DEFAULT NULL,
    #   PRIMARY KEY (`id`),
    #   KEY `degree_degreelevel_degree_id_idx` (`degree_id`),
    #   KEY `degree_degreelevel_degree_level_id_idx` (`level_id`),
    #   CONSTRAINT `degree_degreelevel_degree_id` FOREIGN KEY (`degree_id`) REFERENCES `degree` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
    #   CONSTRAINT `degree_degreelevel_degree_level_id` FOREIGN KEY (`level_id`) REFERENCES `inst_param_value` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
    # ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

    __tablename__ = 'degree_level'
    # id = Column('id', BigInteger, primary_key=True, autoincrement=True)
    degree_level_seq = Sequence('degree_level_seq', increment=1)
    id = Column('id', BigInteger, degree_level_seq, primary_key=True)
    degree_id = Column('degree_id', BigInteger, ForeignKey("degree.id"), nullable=False)
    level_id = Column('level_id', BigInteger, ForeignKey("inst_param_value.id"), nullable=False)
    UniqueConstraint('degree_id', 'level_id')

    def __init__(self, degree_id, level_id):
        self.degree_id = degree_id
        self.level_id = level_id


class Program(Base):
    # CREATE TABLE `program` (
    #   `uuid` varchar(75) DEFAULT NULL,
    #   `id` bigint(20) NOT NULL,
    #   `prog_level_id` bigint(20) DEFAULT NULL,
    #   `degree_id` bigint(20) DEFAULT NULL,
    #   `inst_id` bigint(20) DEFAULT NULL,
    #   `code` VARCHAR(75) DEFAULT NULL,
    #   `name` VARCHAR(75) DEFAULT NULL,
    #   `description` longtext DEFAULT NULL,
    #   `add_prog_fee` tinyint(4) DEFAULT NULL,
    #   `second_lang_req` tinyint(4) DEFAULT NULL,
    #   `first_required_math_course_id` bigint(20) DEFAULT NULL,
    #   `math_intensity` bigint(20) DEFAULT NULL,
    #   `external_link` longtext DEFAULT NULL,
    # `no_of_years` int(11) DEFAULT NULL,
    #   `acad_term_type` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
    #   `no_of_terms_per_year` int(11) DEFAULT NULL,
    #   `status` VARCHAR(75) DEFAULT NULL,
    #   `created_at` datetime DEFAULT NULL,
    #   `created_by` bigint(20) DEFAULT NULL,
    #   `updated_at` datetime DEFAULT NULL,
    #   `updated_by` bigint(20) DEFAULT NULL,
    #   `active` tinyint(1) DEFAULT NULL,
    #   PRIMARY KEY (`id`),
    #   KEY `program_institution_id_idx` (`inst_id`),
    #   KEY `program_degree_id_idx` (`degree_id`),
    #   KEY `program_math_intensity_idx` (`math_intensity`),
    #   KEY `program_program_level_id_idx` (`prog_level_id`),
    #   CONSTRAINT `program_degree_id` FOREIGN KEY (`degree_id`) REFERENCES `degree` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
    #   CONSTRAINT `program_institution_id` FOREIGN KEY (`inst_id`) REFERENCES `institution` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
    #   CONSTRAINT `program_math_intensity` FOREIGN KEY (`math_intensity`) REFERENCES `inst_param_value` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
    #   CONSTRAINT `program_program_level_id` FOREIGN KEY (`prog_level_id`) REFERENCES `inst_param_value` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
    # ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

    __tablename__ = 'program'
    uuid = Column('uuid', VARCHAR(75), unique=True, nullable=True)
    # id = Column('id', BigInteger, primary_key=True, autoincrement=True)
    program_seq = Sequence('program_seq' ,increment=1)
    id = Column('id', BigInteger, program_seq, primary_key=True)
    external_id = Column('external_id', VARCHAR(75), unique=True, nullable=True)
    prog_level_id = Column(BigInteger, ForeignKey("inst_param_value.id"))
    degree_id = Column(BigInteger, ForeignKey("degree.id"))
    inst_id = Column(BigInteger, ForeignKey("institution.id"))
    code = Column('code', VARCHAR(75, collation='utf8mb4_unicode_ci'), nullable=True, default=None)
    name = Column('name', VARCHAR(75, collation='utf8mb4_unicode_ci'), nullable=True, default=None)
    description = Column('description', LONGTEXT(collation='utf8mb4_unicode_ci'), nullable=True, default=None)
    add_prog_fee = Column(Tinyint, nullable=True)
    second_lang_req = Column(Tinyint, nullable=True)
    first_req_math_course_id = Column('first_req_math_course_id', BigInteger, nullable=True)
    math_intensity = Column(BigInteger, ForeignKey("inst_param_value.id"))
    external_link = Column(LONGTEXT, nullable=True)
    no_of_years = Column('no_of_years', INT, nullable=True)
    acad_term_type = Column('acad_term_type', VARCHAR(255, collation='utf8mb4_unicode_ci'), nullable=True, default=None)
    no_of_terms_per_year = Column('no_of_terms_per_year', INT, nullable=True)
    attend_online = Column('attend_online', LONGTEXT(collation='utf8mb4_unicode_ci'), nullable=True, default=None)
    status = Column('status', BigInteger, nullable=True, default=None)
    created_at = Column('created_at', DateTime, nullable=True)
    created_by = Column('created_by', BigInteger, ForeignKey("user.id"))
    updated_at = Column('updated_at', DateTime, nullable=True)
    updated_by = Column('updated_by', BigInteger, ForeignKey("user.id"))
    active = Column('active', Tinyint, nullable=True, default=1)

    def __init__(self, uuid, external_id, prog_level_id, degree_id, inst_id, code, name, description, add_prog_fee,
                 second_lang_req, first_req_math_course_id, math_intensity, external_link,no_of_years,acad_term_type,no_of_terms_per_year,attend_online, created_at, created_by,
                 updated_at, updated_by):
        self.uuid = uuid
        self.external_id = external_id
        self.prog_level_id = prog_level_id
        self.degree_id = degree_id
        self.inst_id = inst_id
        self.code = code
        self.name = name
        self.description = description
        self.add_prog_fee = add_prog_fee
        self.second_lang_req = second_lang_req
        self.first_req_math_course_id = first_req_math_course_id
        self.math_intensity = math_intensity
        self.external_link = external_link
        self.no_of_years = no_of_years
        self.acad_term_type = acad_term_type
        self.no_of_terms_per_year = no_of_terms_per_year
        self.attend_online = attend_online
        self.created_at = created_at
        self.created_by = created_by
        self.updated_at = updated_at
        self.updated_by = updated_by


class Program_area(Base):
    # CREATE TABLE `program_area` (
    #   `program_id` bigint(20) NOT NULL,
    #   `area_id` bigint(20) NOT NULL,
    #   PRIMARY KEY (`program_id`,`area_id`),
    #   KEY `program_area_program_id_idx` (`program_id`),
    #   KEY `program_area_area_id_idx` (`area_id`),
    #   CONSTRAINT `program_area_area_id` FOREIGN KEY (`area_id`) REFERENCES `area` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
    #   CONSTRAINT `program_area_program_id` FOREIGN KEY (`program_id`) REFERENCES `program` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
    # ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    __tablename__ = 'program_area'
    program_id = Column("program_id", BigInteger, ForeignKey("program.id"), primary_key=True)
    area_id = Column("area_id", BigInteger, ForeignKey("area.id"), primary_key=True)

    def __init__(self, program_id, area_id):
        self.program_id = program_id
        self.area_id = area_id


class Program_location(Base):
    # CREATE TABLE `program_location` (
    #   `program_id` bigint(20) NOT NULL,
    #   `location_id` bigint(20) NOT NULL,
    #   PRIMARY KEY (`program_id`,`location_id`),
    #   KEY `program_location_program_id_idx` (`program_id`),
    #   KEY `program_location_location_id_idx` (`location_id`),
    #   CONSTRAINT `program_location_location_id` FOREIGN KEY (`location_id`) REFERENCES `location` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
    #   CONSTRAINT `program_location_program_id` FOREIGN KEY (`program_id`) REFERENCES `program` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
    # ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    __tablename__ = 'program_location'
    program_id = Column("program_id", BigInteger, ForeignKey("program.id"), primary_key=True)
    location_id = Column("location_id", BigInteger, ForeignKey("location.id"), primary_key=True)

    def __init__(self, program_id, location_id):
        self.program_id = program_id
        self.location_id = location_id


class Program_college(Base):
    # CREATE TABLE `program_college` (
    #   `program_id` bigint(20) NOT NULL,
    #   `college_id` bigint(20) NOT NULL,
    #   PRIMARY KEY (`program_id`,`college_id`),
    #   KEY `college_id` (`college_id`),
    #   CONSTRAINT `program_college_ibfk_1` FOREIGN KEY (`program_id`) REFERENCES `program` (`id`),
    #   CONSTRAINT `program_college_ibfk_2` FOREIGN KEY (`college_id`) REFERENCES `institution` (`id`)
    # ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
    __tablename__ = 'program_college'
    program_id = Column("program_id", BigInteger, ForeignKey("program.id"), primary_key=True)
    college_id = Column("college_id", BigInteger, ForeignKey("institution.id"), primary_key=True)

    def __init__(self, program_id, college_id):
        self.program_id = program_id
        self.college_id = college_id


class Requirement_group(Base):
    # CREATE TABLE `rqmt_group` (
    #   `uuid` varchar(75) DEFAULT NULL,
    #   `id` bigint(20) NOT NULL,
    #   `program_id` bigint(20) DEFAULT NULL,
    #   `name` varchar(75) DEFAULT NULL,
    #   `type` VARCHAR(75) DEFAULT NULL,
    #   `credit_type` VARCHAR(75) DEFAULT NULL,
    #   `total_credits` int(11) DEFAULT NULL,
    #   `upper_dev_min` tinyint(4) DEFAULT NULL,
    #   `upper_dev_credits` int(11) DEFAULT NULL,
    #   `tot_cred_at_prov_min` tinyint(4) DEFAULT NULL,
    #   `tot_cred_at_prov` int(11) DEFAULT NULL,
    #   `resi_cred_min` tinyint(4) DEFAULT NULL,
    #   `resi_credits` int(11) DEFAULT NULL,
    #   `tot_comm_coll_cred_min` tinyint(4) DEFAULT NULL,
    #   `tot_comm_coll_cred` int(11) DEFAULT NULL,
    #   `major_gpa_min` tinyint(4) DEFAULT NULL,
    #   `major_gpa` int(11) DEFAULT NULL,
    #   `cumulative_gpa_min` tinyint(4) DEFAULT NULL,
    #   `cumulative_gpa` int(11) DEFAULT NULL,
    #   `external_link` longtext DEFAULT NULL,
    # `academic_year` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
    #   `start_year` int(11) DEFAULT NULL,
    #   `end_year` int(11) DEFAULT NULL,
    #   `created_at` datetime DEFAULT NULL,
    #   `created_by` bigint(20) DEFAULT NULL,
    #   `updated_at` datetime DEFAULT NULL,
    #   `updated_by` bigint(20) DEFAULT NULL,
    #   `active` tinyint(1) DEFAULT NULL,
    #   PRIMARY KEY (`id`),
    #   KEY `requirement_group_program_id_idx` (`program_id`),
    #   CONSTRAINT `requirement_group_program_id` FOREIGN KEY (`program_id`) REFERENCES `program` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
    # ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

    __tablename__ = 'rqmt_group'
    uuid = Column('uuid', VARCHAR(75), unique=True, nullable=True)
    # id = Column('id', BigInteger, primary_key=True, autoincrement=True)
    RQMT_GROUP_seq = Sequence('RQMT_GROUP_seq' ,increment=1)
    id = Column('id', BigInteger, RQMT_GROUP_seq, primary_key=True)
    external_id = Column('external_id', VARCHAR(75), unique=True, nullable=True)
    program_id = Column(BigInteger, ForeignKey("program.id"))
    name = Column('name', VARCHAR(255, collation='utf8mb4_unicode_ci'), nullable=True, default=None)
    code = Column('code', VARCHAR(255, collation='utf8mb4_unicode_ci'), nullable=True, default=None)
    type = Column('type', VARCHAR(75, collation='utf8mb4_unicode_ci'), nullable=True, default=None)
    credit_type = Column('credit_type', VARCHAR(75, collation='utf8mb4_unicode_ci'), nullable=True, default=None)
    total_credits = Column('total_credits', INT, nullable=True)
    upper_dev_min = Column('upper_dev_min', Tinyint, nullable=True)
    upper_dev_credits = Column('upper_dev_credits', INT, nullable=True)
    tot_cred_at_prov_min = Column('tot_cred_at_prov_min', Tinyint, nullable=True)
    tot_cred_at_prov = Column('tot_cred_at_prov', INT, nullable=True)
    resi_cred_min = Column('resi_cred_min', Tinyint, nullable=True)
    resi_credits = Column('resi_credits', INT, nullable=True)
    tot_comm_coll_cred_min = Column('tot_comm_coll_cred_min', Tinyint, nullable=True)
    tot_comm_coll_cred = Column('tot_comm_coll_cred', INT, nullable=True)
    major_gpa_min = Column('major_gpa_min', Tinyint, nullable=True)
    major_gpa = Column('major_gpa', INT, nullable=True)
    cumulative_gpa_min = Column('cumulative_gpa_min', Tinyint, nullable=True)
    cumulative_gpa = Column('cumulative_gpa', INT, nullable=True)
    external_link = Column(LONGTEXT, nullable=True)
    academic_year = Column('academic_year', VARCHAR(255, collation='utf8mb4_unicode_ci'), nullable=True, default=None)
    start_year = Column('start_year', INT, nullable=True)
    end_year = Column('end_year', INT, nullable=True)
    created_at = Column('created_at', DateTime, nullable=True)
    created_by = Column('created_by', BigInteger, ForeignKey("user.id"))
    updated_at = Column('updated_at', DateTime, nullable=True)
    updated_by = Column('updated_by', BigInteger, ForeignKey("user.id"))
    active = Column('active', Tinyint, nullable=True, default=1)

    def __init__(self, uuid, external_id, program_id, name,code, type, credit_type, total_credits, upper_dev_min,
                 upper_dev_credits, tot_cred_at_prov_min, tot_cred_at_prov, resi_cred_min, resi_credits,
                 tot_comm_coll_cred_min, tot_comm_coll_cred, major_gpa_min, major_gpa, cumulative_gpa_min,
                 cumulative_gpa, external_link,academic_year, start_year, end_year, created_at, created_by, updated_at, updated_by):
        self.uuid = uuid
        self.external_id = external_id
        self.program_id = program_id
        self.name = name
        self.code = code
        self.type = type
        self.credit_type = credit_type
        self.total_credits = total_credits
        self.upper_dev_min = upper_dev_min
        self.upper_dev_credits = upper_dev_credits
        self.tot_cred_at_prov_min = tot_cred_at_prov_min
        self.tot_cred_at_prov = tot_cred_at_prov
        self.resi_cred_min = resi_cred_min
        self.resi_credits = resi_credits
        self.tot_comm_coll_cred_min = tot_comm_coll_cred_min
        self.tot_comm_coll_cred = tot_comm_coll_cred
        self.major_gpa_min = major_gpa_min
        self.major_gpa = major_gpa
        self.cumulative_gpa_min = cumulative_gpa_min
        self.cumulative_gpa = cumulative_gpa
        self.external_link = external_link
        self.academic_year = academic_year
        self.start_year = start_year
        self.end_year = end_year
        self.created_at = created_at
        self.created_by = created_by
        self.updated_at = updated_at
        self.updated_by = updated_by


class Term(Base):
    # CREATE TABLE `term` (
    #   `uuid` varchar(75) DEFAULT NULL,
    #   `id` bigint(20) NOT NULL,
    #   `requirement_group_id` bigint(20) DEFAULT NULL,
    #   `name` VARCHAR(75) DEFAULT NULL,
    #   `main` VARCHAR(75) DEFAULT NULL,
    #   `part` VARCHAR(75) DEFAULT NULL,
    #   `credit_type` VARCHAR(75) DEFAULT NULL,
    #   `min_credits` int(11) DEFAULT NULL,
    #   `max_credits` int(11) DEFAULT NULL,
    #   `total_credits` int(11) DEFAULT NULL,
    #   `parent_id` bigint(20) DEFAULT NULL,
    #   `year` int(11) DEFAULT NULL,
    #   `created_at` datetime DEFAULT NULL,
    #   `created_by` bigint(20) DEFAULT NULL,
    #   `updated_at` datetime DEFAULT NULL,
    #   `updated_by` bigint(20) DEFAULT NULL,
    #   `active` tinyint(4) DEFAULT NULL,
    #   PRIMARY KEY (`id`),
    #   KEY `term_requirement_group_id_idx` (`requirement_group_id`),
    #   KEY `term_created_by_idx` (`created_by`),
    #   KEY `term_updated_by_idx` (`updated_by`),
    #   CONSTRAINT `term_created_by` FOREIGN KEY (`created_by`) REFERENCES `user` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
    #   CONSTRAINT `term_requirement_group_id` FOREIGN KEY (`requirement_group_id`) REFERENCES `rqmt_group` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
    #   CONSTRAINT `term_updated_by` FOREIGN KEY (`updated_by`) REFERENCES `user` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
    # ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

    __tablename__ = 'term'
    uuid = Column('uuid', VARCHAR(75), unique=True, nullable=True)
    # id = Column('id', BigInteger, primary_key=True, autoincrement=True)
    TERM_seq = Sequence('TERM_seq' ,increment=1)
    id = Column('id', BigInteger, TERM_seq, primary_key=True)
    external_id = Column('external_id', VARCHAR(75), unique=True, nullable=True)
    requirement_group_id = Column(BigInteger, ForeignKey("rqmt_group.id"))
    name = Column('name', VARCHAR(75, collation='utf8mb4_unicode_ci'), nullable=True, default=None)
    main = Column('main', VARCHAR(75, collation='utf8mb4_unicode_ci'), nullable=True, default=None)
    part = Column('part', VARCHAR(75, collation='utf8mb4_unicode_ci'), nullable=True, default=None)
    credit_type = Column('credit_type', VARCHAR(75, collation='utf8mb4_unicode_ci'), nullable=True, default=None)
    min_credits = Column('min_credits', Float, nullable=True)
    max_credits = Column('max_credits', Float, nullable=True)
    total_credits_min = Column('total_credits_min', INT, nullable=True)
    total_credits_max = Column('total_credits_max', INT, nullable=True)
    year = Column('year', INT, nullable=True)
    created_at = Column('created_at', DateTime, nullable=True)
    created_by = Column('created_by', BigInteger, ForeignKey("user.id"))
    updated_at = Column('updated_at', DateTime, nullable=True)
    updated_by = Column('updated_by', BigInteger, ForeignKey("user.id"))
    active = Column('active', Tinyint, nullable=True, default=1)

    def __init__(self, uuid, external_id, requirement_group_id, name, main, part, credit_type, min_credits, max_credits,
                 total_credits_min, total_credits_max, year, created_at, created_by, updated_at, updated_by):
        self.uuid = uuid
        self.external_id = external_id
        self.requirement_group_id = requirement_group_id
        self.name = name
        self.main = main
        self.part = part
        self.credit_type = credit_type
        self.min_credits = min_credits
        self.max_credits = max_credits
        self.total_credits_min = total_credits_min
        self.total_credits_max = total_credits_max
        self.year = year
        self.created_at = created_at
        self.created_by = created_by
        self.updated_at = updated_at
        self.updated_by = updated_by


class Requirement(Base):
    # CREATE TABLE `requirement` (
    #   `uuid` varchar(75) CHARACTER SET utf8mb3 DEFAULT NULL,
    #   `id` bigint(20) NOT NULL,
    # `rqmt_category_id` bigint(20) DEFAULT NULL,
    #   `text` varchar(200) CHARACTER SET utf8mb3 DEFAULT NULL,
    #   `expression` VARCHAR(75) CHARACTER SET utf8mb3 DEFAULT NULL,
    #   `credity_type` VARCHAR(75) CHARACTER SET utf8mb3 DEFAULT NULL,
    #   `min_credits` int(11) DEFAULT NULL,
    #   `max_credits` int(11) DEFAULT NULL,
    #   `minimum_grade` VARCHAR(75) CHARACTER SET utf8mb3 DEFAULT NULL,
    #   `critical_course` tinyint(4) DEFAULT NULL,
    #   `necessary_course` tinyint(4) DEFAULT NULL,
    # proposed_rqmt` tinyint(4) DEFAULT NULL,
    #   `created_at` datetime DEFAULT NULL,
    #   `created_by` bigint(20) DEFAULT NULL,
    #   `updated_at` datetime DEFAULT NULL,
    #   `updated_by` bigint(20) DEFAULT NULL,
    #   `active` tinyint(4) DEFAULT NULL,
    #   PRIMARY KEY (`id`)

    # ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

    __tablename__ = 'requirement'
    uuid = Column('uuid', VARCHAR(75), unique=True, nullable=True)
    # id = Column('id', BigInteger, primary_key=True, autoincrement=True)
    requirement_seq = Sequence('requirement_seq' ,increment=1)
    id = Column('id', BigInteger, requirement_seq, primary_key=True)
    external_id = Column('external_id', VARCHAR(75), unique=True, nullable=True)
    rqmt_group_id = Column('rqmt_group_id', BigInteger, ForeignKey("rqmt_group.id"))
    rqmt_group_rqmt_category_id = Column('rqmt_group_rqmt_category_id', BigInteger, ForeignKey("rqmt_group_rqmt_category.id"))
    # rqmt_category_id = Column('rqmt_category_id', BigInteger, ForeignKey("rqmt_category.id"))
    text = Column('text', LONGTEXT(collation='utf8mb4_unicode_ci'), nullable=True)
    expression = Column('expression', VARCHAR(255, collation='utf8mb4_unicode_ci'), nullable=True)
    credit_type = Column('credit_type', VARCHAR(75, collation='utf8mb4_unicode_ci'), nullable=True)
    min_credits = Column('min_credits', Float, nullable=True)
    max_credits = Column('max_credits', Float, nullable=True)
    minimum_grade = Column('minimum_grade', VARCHAR(75, collation='utf8mb4_unicode_ci'), nullable=True)
    critical_course = Column('critical_course', Tinyint, nullable=True)
    necessary_course = Column('necessary_course', Tinyint, nullable=True)
    proposed_rqmt = Column('proposed_rqmt', Tinyint, nullable=True, default=0)
    created_at = Column('created_at', DateTime, nullable=True)
    created_by = Column('created_by', BigInteger, ForeignKey("user.id"))
    updated_at = Column('updated_at', DateTime, nullable=True)
    updated_by = Column('updated_by', BigInteger, ForeignKey("user.id"))
    active = Column('active', Tinyint, nullable=True, default=1)

    def __init__(self, uuid, external_id, rqmt_group_id, rqmt_group_rqmt_category_id, text, expression, credit_type, min_credits, max_credits,
                 minimum_grade,critical_course,necessary_course, created_at, created_by, updated_at, updated_by):
        self.uuid = uuid
        self.external_id = external_id
        self.rqmt_group_id = rqmt_group_id
        self.rqmt_group_rqmt_category_id = rqmt_group_rqmt_category_id
        self.text = text
        self.expression = expression
        self.credit_type = credit_type
        self.min_credits = min_credits
        self.max_credits = max_credits
        self.minimum_grade = minimum_grade
        self.critical_course = critical_course
        self.necessary_course = necessary_course
        self.created_at = created_at
        self.created_by = created_by
        self.updated_at = updated_at
        self.updated_by = updated_by


class Requirement_term(Base):
    # CREATE TABLE `rqmt_term` (
    #   `requirement_id` bigint(20) NOT NULL,
    #   `term_id` bigint(20) NOT NULL,
    #   PRIMARY KEY (`requirement_id`,`term_id`),
    #   KEY `term_requirement_term_id_idx` (`term_id`),
    #   KEY `term_requirement_requirement_id_idx` (`requirement_id`),
    #   CONSTRAINT `term_requirement_requirement_id` FOREIGN KEY (`requirement_id`) REFERENCES `requirement` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
    #   CONSTRAINT `term_requirement_term_id` FOREIGN KEY (`term_id`) REFERENCES `term` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
    # ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

    __tablename__ = 'rqmt_term'
    requirement_id = Column('requirement_id', BigInteger, ForeignKey("requirement.id"), primary_key=True)
    term_id = Column('term_id', BigInteger, ForeignKey("term.id"), primary_key=True)

    def __init__(self, requirement_id, term_id):
        self.requirement_id = requirement_id
        self.term_id = term_id


class Rqmt_group_college(Base):
    # CREATE TABLE `rqmt_group_college` (
    #   `rqmt_group_id` bigint(20) NOT NULL,
    #   `college_id` bigint(20) NOT NULL,
    #   PRIMARY KEY (`rqmt_group_id`,`college_id`),
    #   KEY `rqmt_group_college_rqmt_college_id` (`college_id`),
    #   CONSTRAINT `rqmt_group_college_rqmt_college_id` FOREIGN KEY (`college_id`) REFERENCES `institution` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
    #   CONSTRAINT `rqmt_group_college_rqmt_group_id` FOREIGN KEY (`rqmt_group_id`) REFERENCES `rqmt_group` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
    # ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
    # /*!40101 SET character_set_client = @saved_cs_client */;

    __tablename__ = 'rqmt_group_college'
    rqmt_group_id = Column('rqmt_group_id', BigInteger, ForeignKey("rqmt_group.id"), primary_key=True)
    college_id = Column('college_id', BigInteger, ForeignKey("institution.id"), primary_key=True)

    def __init__(self, rqmt_group_id, college_id):
        self.rqmt_group_id = rqmt_group_id
        self.college_id = college_id


class Rqmt_group_location(Base):

    # CREATE TABLE `rqmt_group_location` (
    #   `rqmt_group_id` bigint(20) NOT NULL,
    #   `location_id` bigint(20) NOT NULL,
    #   PRIMARY KEY (`rqmt_group_id`,`location_id`),
    #   KEY `rqmt_group_location_location_id` (`location_id`),
    #   CONSTRAINT `rqmt_group_location_location_id` FOREIGN KEY (`location_id`) REFERENCES `location` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
    #   CONSTRAINT `rqmt_group_location_rqmt_group_id` FOREIGN KEY (`rqmt_group_id`) REFERENCES `rqmt_group` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
    # ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
    __tablename__ = 'rqmt_group_location'
    rqmt_group_id = Column('rqmt_group_id', BigInteger, ForeignKey("rqmt_group.id"), primary_key=True)
    location_id = Column('location_id', BigInteger, ForeignKey("location.id"), primary_key=True)

    def __init__(self, rqmt_group_id, location_id):
        self.rqmt_group_id = rqmt_group_id
        self.location_id = location_id


class Department(Base):
    # CREATE TABLE `department` (
    #   `uuid` varchar(75) DEFAULT NULL,
    #   `id` bigint(20) NOT NULL,
    #   `inst_id` bigint(20) DEFAULT NULL,
    #   `name` varchar(45) DEFAULT NULL,
    #   `code` varchar(45) DEFAULT NULL,
    #   `created_at` datetime DEFAULT NULL,
    #   `created_by` bigint(20) DEFAULT NULL,
    #   `updated_at` datetime DEFAULT NULL,
    #   `updated_by` bigint(20) DEFAULT NULL,
    #   `active` tinyint(1) DEFAULT NULL,
    #   PRIMARY KEY (`id`),
    #   KEY `department_institution_id_idx` (`inst_id`),
    #   KEY `department_created_by_idx` (`created_by`),
    #   KEY `department_updated_by_idx` (`updated_by`),
    #   CONSTRAINT `department_created_by` FOREIGN KEY (`created_by`) REFERENCES `user` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
    #   CONSTRAINT `department_institution_id` FOREIGN KEY (`inst_id`) REFERENCES `institution` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
    #   CONSTRAINT `department_updated_by` FOREIGN KEY (`updated_by`) REFERENCES `user` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
    # ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    __tablename__ = 'department'
    uuid = Column('uuid', VARCHAR(75), unique=True, nullable=True)
    # id = Column('id', BigInteger, primary_key=True, autoincrement=True)
    DEPARTMENT_seq = Sequence('DEPARTMENT_seq' ,increment=1)
    id = Column('id', BigInteger, DEPARTMENT_seq, primary_key=True)
    external_id = Column('external_id', VARCHAR(75), unique=True, nullable=True)
    inst_id = Column(BigInteger, ForeignKey("institution.id"))
    name = Column('name', VARCHAR(75, collation='utf8mb4_unicode_ci'), nullable=True, default=None)
    code = Column('code', VARCHAR(75, collation='utf8mb4_unicode_ci'), nullable=True, default=None)
    created_at = Column('created_at', DateTime, nullable=True)
    created_by = Column('created_by', BigInteger, ForeignKey("user.id"))
    updated_at = Column('updated_at', DateTime, nullable=True)
    updated_by = Column('updated_by', BigInteger, ForeignKey("user.id"))
    active = Column('active', Tinyint, nullable=True, default=1)

    def __init__(self, uuid, external_id, inst_id, name, code, created_at, created_by, updated_at, updated_by):
        self.uuid = uuid
        self.external_id = external_id
        self.inst_id = inst_id
        self.name = name
        self.code = code
        self.created_at = created_at
        self.created_by = created_by
        self.updated_at = updated_at
        self.updated_by = updated_by


class Course(Base):
    # CREATE TABLE `course` (
    #   `uuid` varchar(75) DEFAULT NULL,
    #   `id` bigint(20) NOT NULL,
    #   `inst_id` bigint(20) DEFAULT NULL,
    #   `name` varchar(45) DEFAULT NULL,
    #   `code` varchar(45) DEFAULT NULL,
    #   `code_prefix` varchar(45) DEFAULT NULL,
    #   `dept_id` bigint(20) DEFAULT NULL,
    #   `course_desc` longtext DEFAULT NULL,
    #   `min_units` int(11) DEFAULT NULL,
    #   `max_units` int(11) DEFAULT NULL,
    #   `external_link` longtext DEFAULT NULL,
    #   `created_at` datetime DEFAULT NULL,
    #   `created_by` bigint(20) DEFAULT NULL,
    #   `updated_at` datetime DEFAULT NULL,
    #   `updated_by` bigint(20) DEFAULT NULL,
    #   `active` tinyint(1) DEFAULT NULL,
    #   PRIMARY KEY (`id`),
    #   KEY `course_institution_id_idx` (`inst_id`),
    #   KEY `course_dept_id_idx` (`dept_id`),
    #   KEY `course_created_by_idx` (`created_by`),
    #   KEY `course_updated_by_idx` (`updated_by`),
    #   CONSTRAINT `course_created_by` FOREIGN KEY (`created_by`) REFERENCES `user` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
    #   CONSTRAINT `course_dept_id` FOREIGN KEY (`dept_id`) REFERENCES `department` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
    #   CONSTRAINT `course_institution_id` FOREIGN KEY (`inst_id`) REFERENCES `institution` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
    #   CONSTRAINT `course_updated_by` FOREIGN KEY (`updated_by`) REFERENCES `user` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
    # ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

    __tablename__ = 'course'
    uuid = Column('uuid', VARCHAR(75), unique=True, nullable=True)
    # id = Column('id', BigInteger, primary_key=True, autoincrement=True)
    course_seq = Sequence('course_seq' ,increment=1)
    id = Column('id', BigInteger, course_seq, primary_key=True)
    external_id = Column('external_id', VARCHAR(75), unique=True, nullable=True)
    inst_id = Column(BigInteger, ForeignKey("institution.id"))
    name = Column('name', VARCHAR(255, collation='utf8mb4_unicode_ci'), nullable=True, default=None)
    code = Column('code', VARCHAR(75, collation='utf8mb4_unicode_ci'), nullable=True, default=None)
    code_prefix = Column('code_prefix', VARCHAR(75, collation='utf8mb4_unicode_ci'), nullable=True, default=None)
    code_suffix = Column('code_suffix', INT, nullable=True)
    dept_id = Column(BigInteger, ForeignKey("department.id"), nullable=True, default=None)
    course_desc = Column('course_desc', LONGTEXT(collation='utf8mb4_unicode_ci'), nullable=True, default=None)
    credit = Column('credit', Tinyint, nullable=True, default=None)
    credit_type = Column('credit_type', VARCHAR(75, collation='utf8mb4_unicode_ci'), nullable=True)
    min_credits = Column('min_credits', Float, nullable=True)
    max_credits = Column('max_credits', Float, nullable=True)
    external_link = Column('external_link', LONGTEXT(collation='utf8mb4_unicode_ci'), nullable=True, default=None)
    gs_expression = Column('gs_expression', VARCHAR(75, collation='utf8mb4_unicode_ci'), nullable=True, default=None)
    program = Column('program', VARCHAR(255, collation='utf8mb4_unicode_ci'), nullable=True, default=None)
    level_id = Column('level_id', BigInteger, ForeignKey("inst_param_value.id"))
    created_at = Column('created_at', DateTime, nullable=True)
    created_by = Column('created_by', BigInteger, ForeignKey("user.id"))
    updated_at = Column('updated_at', DateTime, nullable=True)
    updated_by = Column('updated_by', BigInteger, ForeignKey("user.id"))
    active = Column('active', Tinyint, nullable=True, default=1)

    def __init__(self, uuid, external_id, inst_id, name, code, code_prefix, code_suffix, dept_id, course_desc, credit, credit_type,
                 min_credits, max_credits, external_link, gs_expression, program, level_id, created_at, created_by, updated_at, updated_by):
        self.uuid = uuid
        self.external_id = external_id
        self.inst_id = inst_id
        self.name = name
        self.code = code
        self.code_prefix = code_prefix
        self.code_suffix = code_suffix
        self.dept_id = dept_id
        self.course_desc = course_desc
        self.credit = credit
        self.credit_type = credit_type
        self.min_credits = min_credits
        self.max_credits = max_credits
        self.external_link = external_link
        self.gs_expression = gs_expression
        self.program = program
        self.level_id = level_id
        self.created_at = created_at
        self.created_by = created_by
        self.updated_at = updated_at
        self.updated_by = updated_by


class Course_additional_detail(Base):
    # CREATE TABLE `course_additional_detail` (
    #   `id` bigint(20) NOT NULL,
    #   `field_name` varchar(45) CHARACTER SET utf8mb3 DEFAULT NULL,
    #   `field_value` varchar(45) CHARACTER SET utf8mb3 DEFAULT NULL,
    #   PRIMARY KEY (`id`)
    # ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

    __tablename__ = 'course_additional_detail'
    # id = Column('id', BigInteger, primary_key=True, autoincrement=True)
    COURSE_ADDITIONAL_DETAIL_seq = Sequence('COURSE_ADDITIONAL_DETAIL_seq' ,increment=1)
    id = Column('id', BigInteger, COURSE_ADDITIONAL_DETAIL_seq, primary_key=True)
    field_name = Column('field_name', VARCHAR(45, collation='utf8mb4_unicode_ci'), nullable=True, default=None)
    field_value = Column('field_value', VARCHAR(45, collation='utf8mb4_unicode_ci'), nullable=True, default=None)

    def __init__(self, field_name, field_value):
        self.field_name = field_name
        self.field_value = field_value


class Course_college(Base):
    # CREATE TABLE `course_college` (
    #   `id` bigint(20) NOT NULL,
    #   `course_id` bigint(20) DEFAULT NULL,
    #   `college_id` bigint(20) DEFAULT NULL,
    #   `prerequisites` longtext COLLATE utf8mb4_unicode_ci DEFAULT NULL,
    #   PRIMARY KEY (`id`),
    #   KEY `course_college_course_id` (`course_id`),
    #   KEY `course_college_college_id` (`college_id`),
    #   CONSTRAINT `course_college_college_id` FOREIGN KEY (`college_id`) REFERENCES `institution` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
    #   CONSTRAINT `course_college_course_id` FOREIGN KEY (`course_id`) REFERENCES `course` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
    # ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

    __tablename__ = 'course_college'
    Course_college_seq = Sequence('Course_college_seq', increment=1)
    id = Column('id', BigInteger, Course_college_seq, primary_key=True)
    course_id = Column('course_id', BigInteger, ForeignKey("course.id"), primary_key=True)
    college_id= Column('college_id', BigInteger, ForeignKey("institution.id"), primary_key=True)
    prerequisite = Column('prerequisite', LONGTEXT(collation='utf8mb4_unicode_ci'), nullable=True, default=None)
    dept_name = Column('dept_name', VARCHAR(255, collation='utf8mb4_unicode_ci'), nullable=True, default=None)

    def __init__(self, course_id, college_id, prerequisite, dept_name):
        self.course_id = course_id
        self.college_id = college_id
        self.prerequisite = prerequisite
        self.dept_name = dept_name


class Course_gs_category(Base):
    # CREATE TABLE `course_gs_category` (
    #   `course_id` bigint(20) NOT NULL,
    #   `gs_ctgry_id` bigint(20) NOT NULL,
    #   PRIMARY KEY (`course_id`,`gs_ctgry_id`),
    #   KEY `course_gs_category_course_id_idx` (`course_id`),
    #   KEY `course_gs_category_gs_category_id_idx` (`gs_ctgry_id`),
    #   CONSTRAINT `course_gs_category_course_id` FOREIGN KEY (`course_id`) REFERENCES `course` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
    #   CONSTRAINT `course_gs_category_gs_category_id` FOREIGN KEY (`gs_ctgry_id`) REFERENCES `gs_category` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
    # ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

    __tablename__ = 'course_gs_category'
    course_id = Column('course_id', BigInteger, ForeignKey("course.id"), primary_key=True)
    gs_ctgry_id = Column('gs_ctgry_id', BigInteger, ForeignKey("gs_category.id"), primary_key=True)

    def __init__(self, course_id, gs_ctgry_id):
        self.course_id = course_id
        self.gs_ctgry_id = gs_ctgry_id


class Gs_category(Base):
    # CREATE TABLE `gs_category` (
    #   `uuid` varchar(75) DEFAULT NULL,
    #   `id` bigint(20) NOT NULL,
    # `inst_id` BIGINT(20) DEFAULT NULL AFTER `external_id`;
    #   `code` varchar(45) DEFAULT NULL,
    #   `abbreviation` varchar(45) DEFAULT NULL,
    #   `created_at` datetime DEFAULT NULL,
    #   `created_by` bigint(20) DEFAULT NULL,
    #   `updated_at` datetime DEFAULT NULL,
    #   `updated_by` bigint(20) DEFAULT NULL,
    #   `active` tinyint(1) DEFAULT NULL,
    #   PRIMARY KEY (`id`),
    #   KEY `gs_category_created_by_idx` (`created_by`),
    #   KEY `gs_category_updated_by_idx` (`updated_by`),
    #   CONSTRAINT `gs_category_created_by` FOREIGN KEY (`created_by`) REFERENCES `user` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
    #   CONSTRAINT `gs_category_updated_by` FOREIGN KEY (`updated_by`) REFERENCES `user` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
    # ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

    __tablename__ = 'gs_category'
    uuid = Column('uuid', VARCHAR(75), unique=True, nullable=True)
    # id = Column('id', BigInteger, primary_key=True, autoincrement=True)
    gs_category_seq = Sequence('gs_category_seq' ,increment=1)
    id = Column('id', BigInteger, gs_category_seq, primary_key=True)
    external_id = Column('external_id', VARCHAR(75), unique=True, nullable=True)
    inst_id = Column('inst_id', BigInteger, ForeignKey("institution.id"))
    code = Column('code', VARCHAR(75, collation='utf8mb4_unicode_ci'), nullable=True, default=None)
    abbreviation = Column('abbreviation', VARCHAR(255), nullable=True, default=None)
    created_at = Column('created_at', DateTime, nullable=True)
    created_by = Column('created_by', BigInteger, ForeignKey("user.id"))
    updated_at = Column('updated_at', DateTime, nullable=True)
    updated_by = Column('updated_by', BigInteger, ForeignKey("user.id"))
    active = Column('active', Tinyint, nullable=True, default=1)

    def __init__(self, uuid, external_id, inst_id, code, abbreviation, created_at, created_by, updated_at, updated_by):
        self.uuid = uuid
        self.external_id = external_id
        self.inst_id = inst_id
        self.code = code
        self.abbreviation = abbreviation
        self.created_at = created_at
        self.created_by = created_by
        self.updated_at = updated_at
        self.updated_by = updated_by


class Notes(Base):
    # CREATE TABLE `notes` (
    #   `uuid` varchar(75) DEFAULT NULL,
    #   `id` bigint(20) NOT NULL,
    #   `entity_type` varchar(45) DEFAULT NULL,
    #   `entity_id` bigint(20) DEFAULT NULL,
    #   `value` longtext DEFAULT NULL,
    #   `created_at` datetime DEFAULT NULL,
    #   `created_by` bigint(20) DEFAULT NULL,
    #   `updated_at` datetime DEFAULT NULL,
    #   `updated_by` bigint(20) DEFAULT NULL,
    #   `active` tinyint(1) DEFAULT NULL,
    #   PRIMARY KEY (`id`),
    #   KEY `notes_created_by_idx` (`created_by`),
    #   KEY `notes_updated_by_idx` (`updated_by`),
    #   CONSTRAINT `notes_created_by` FOREIGN KEY (`created_by`) REFERENCES `user` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
    #   CONSTRAINT `notes_updated_by` FOREIGN KEY (`updated_by`) REFERENCES `user` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
    # ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    __tablename__ = 'notes'
    # id = Column('id', BigInteger, primary_key=True, autoincrement=True)
    NOTES_seq = Sequence('NOTES_seq',increment=1)
    id = Column('id', BigInteger, NOTES_seq, primary_key=True)
    entity_type = Column('entity_type', VARCHAR(45, collation='utf8mb4_unicode_ci'), nullable=True, default=None)
    entity_id = Column('entity_id', BigInteger, nullable=True, default=None)
    value = Column('value', LONGTEXT(collation='utf8mb4_unicode_ci'), nullable=True, default=None)
    created_at = Column('created_at', DateTime, nullable=True)
    created_by = Column('created_by', BigInteger, ForeignKey("user.id"))
    updated_at = Column('updated_at', DateTime, nullable=True)
    updated_by = Column('updated_by', BigInteger, ForeignKey("user.id"))
    active = Column('active', Tinyint, nullable=True, default=1)

    def __init__(self, entity_type, entity_id, value, created_at, created_by, updated_at, updated_by):
        self.entity_type = entity_type
        self.entity_id = entity_id
        self.value = value
        self.created_at = created_at
        self.created_by = created_by
        self.updated_at = updated_at
        self.updated_by = updated_by


class Requirement_variable(Base):
    # CREATE TABLE `rqmt_variable` (
    #   `uuid` varchar(75) DEFAULT NULL,
    #   `id` bigint(20) NOT NULL AUTO_INCREMENT,
    #   `requirement_id` bigint(20) DEFAULT NULL,
    #   `name` varchar(75) DEFAULT NULL,
    #   `entity` varchar(75) DEFAULT NULL,
    #   `value` varchar(75) DEFAULT NULL,
    #   `created_at` datetime DEFAULT NULL,
    #   `created_by` bigint(20) DEFAULT NULL,
    #   `updated_at` datetime DEFAULT NULL,
    #   `updated_by` bigint(20) DEFAULT NULL,
    #   `active` tinyint(1) DEFAULT NULL,
    #   PRIMARY KEY (`id`),
    #   KEY `requirement_variables_requirement_id_idx` (`requirement_id`),
    #   KEY `requirement_variables_created_by_idx` (`created_by`),
    #   KEY `requirement_variables_updated_by_idx` (`updated_by`),
    #   CONSTRAINT `requirement_variables_created_by` FOREIGN KEY (`created_by`) REFERENCES `user` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
    #   CONSTRAINT `requirement_variables_requirement_id` FOREIGN KEY (`requirement_id`) REFERENCES `requirement` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
    #   CONSTRAINT `requirement_variables_updated_by` FOREIGN KEY (`updated_by`) REFERENCES `user` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
    # ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

    __tablename__ = 'rqmt_variable'
    uuid = Column('uuid', VARCHAR(75), unique=True, nullable=True)
    external_id = Column('external_id', VARCHAR(75), unique=True, nullable=True)
    # id = Column('id', BigInteger, primary_key=True, autoincrement=True)
    RQMT_VARIABLE_seq = Sequence('RQMT_VARIABLE_seq', increment=1)
    id = Column('id', BigInteger, RQMT_VARIABLE_seq, primary_key=True)
    requirement_id = Column('requirement_id', BigInteger, ForeignKey("requirement.id"))
    name = Column('name', VARCHAR(255), nullable=True, default=None)
    entity = Column('entity', VARCHAR(75), nullable=True, default=None)
    value = Column('value', BigInteger, nullable=True, default=None)
    created_at = Column('created_at', DateTime, nullable=True)
    created_by = Column('created_by', BigInteger, ForeignKey("user.id"))
    updated_at = Column('updated_at', DateTime, nullable=True)
    updated_by = Column('updated_by', BigInteger, ForeignKey("user.id"))
    active = Column('active', Tinyint, nullable=True, default=1)

    def __init__(self, uuid, external_id, requirement_id, name, entity, value, created_at, created_by, updated_at,
                 updated_by):
        self.uuid = uuid
        self.external_id = external_id
        self.requirement_id = requirement_id
        self.name = name
        self.entity = entity
        self.value = value
        self.created_at = created_at
        self.created_by = created_by
        self.updated_at = updated_at
        self.updated_by = updated_by


class Graduate_req_category(Base):
    # CREATE TABLE `rqmt_category` (
    #   `id` bigint(20) NOT NULL,
    #   `uuid` varchar(75) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
    #   `external_id` varchar(75) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
    #   `inst_id` bigint(20) DEFAULT NULL,
    #   `name` varchar(75) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
    #   `created_at` datetime DEFAULT NULL,
    #   `created_by` bigint(20) DEFAULT NULL,
    #   `updated_at` datetime DEFAULT NULL,
    #   `updated_by` bigint(20) DEFAULT NULL,
    #   `active` tinyint(4) DEFAULT NULL,
    #   PRIMARY KEY (`id`),
    #   UNIQUE KEY `uuid` (`uuid`),
    #   UNIQUE KEY `external_id` (`external_id`),
    #   KEY `inst_id` (`inst_id`),
    #   KEY `created_by` (`created_by`),
    #   KEY `updated_by` (`updated_by`),
    #   CONSTRAINT `rqmt_category_ibfk_1` FOREIGN KEY (`inst_id`) REFERENCES `institution` (`id`),
    #   CONSTRAINT `rqmt_category_ibfk_2` FOREIGN KEY (`created_by`) REFERENCES `user` (`id`),
    #   CONSTRAINT `rqmt_category_ibfk_3` FOREIGN KEY (`updated_by`) REFERENCES `user` (`id`)
    # ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
    __tablename__ = 'rqmt_category'
    uuid = Column('uuid', VARCHAR(75), unique=True, nullable=True)
    rqmt_category_seq = Sequence('rqmt_category_seq', increment=1)
    id = Column('id', BigInteger, rqmt_category_seq, primary_key=True)
    external_id = Column('external_id', VARCHAR(75), unique=True, nullable=True)
    inst_id = Column('inst_id', BigInteger, ForeignKey("institution.id"))
    name = Column('name', LONGTEXT(collation='utf8mb4_unicode_ci'), nullable=True, default=None)
    created_at = Column('created_at', DateTime, nullable=True)
    created_by = Column('created_by', BigInteger, ForeignKey("user.id"))
    updated_at = Column('updated_at', DateTime, nullable=True)
    updated_by = Column('updated_by', BigInteger, ForeignKey("user.id"))
    active = Column('active', Tinyint, nullable=True, default=1)

    def __init__(self, uuid, external_id, inst_id, name, created_at, created_by, updated_at, updated_by):
        # self.id = id
        self.uuid = uuid
        self.external_id = external_id
        self.inst_id = inst_id
        self.name = name
        self.created_at = created_at
        self.created_by = created_by
        self.updated_at = updated_at
        self.updated_by = updated_by


class Admission_req(Base):
    # CREATE TABLE `admission_req` (
    #   `uuid` varchar(75) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
    #   `id` bigint(20) NOT NULL,
    #   `external_id` varchar(75) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
    #   `program_id` bigint(20) DEFAULT NULL,
    #   `description` longtext COLLATE utf8mb4_unicode_ci DEFAULT NULL,
    #   `created_at` datetime DEFAULT NULL,
    #   `created_by` bigint(20) DEFAULT NULL,
    #   `updated_at` datetime DEFAULT NULL,
    #   `updated_by` bigint(20) DEFAULT NULL,
    #   `active` tinyint(4) DEFAULT NULL,
    #   PRIMARY KEY (`id`),
    #   UNIQUE KEY `uuid` (`uuid`),
    #   UNIQUE KEY `external_id` (`external_id`),
    #   KEY `created_by` (`created_by`),
    #   KEY `updated_by` (`updated_by`),
    #   KEY `admission_req_ibfk_3` (`program_id`),
    #   CONSTRAINT `admission_req_ibfk_1` FOREIGN KEY (`created_by`) REFERENCES `user` (`id`),
    #   CONSTRAINT `admission_req_ibfk_2` FOREIGN KEY (`updated_by`) REFERENCES `user` (`id`),
    #   CONSTRAINT `admission_req_ibfk_3` FOREIGN KEY (`program_id`) REFERENCES `program` (`id`)
    # ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

    __tablename__ = 'Admission_req'

    uuid = Column('uuid', VARCHAR(75), unique=True, nullable=True)
    Admission_req_seq = Sequence('Admission_req_seq', increment=1)
    id = Column('id', BigInteger, Admission_req_seq, primary_key=True)
    external_id = Column('external_id', VARCHAR(75), unique=True, nullable=True)
    program_id = Column('program_id', BigInteger, ForeignKey("program.id"))
    description = Column('description', LONGTEXT(collation='utf8mb4_unicode_ci'), nullable=True, default=None)
    created_at = Column('created_at', DateTime, nullable=True)
    created_by = Column('created_by', BigInteger, ForeignKey("user.id"))
    updated_at = Column('updated_at', DateTime, nullable=True)
    updated_by = Column('updated_by', BigInteger, ForeignKey("user.id"))
    active = Column('active', Tinyint, nullable=True, default=1)

    def __init__(self,uuid, external_id, program_id, description, created_at, created_by, updated_at, updated_by):
        # self.id = id
        self.uuid = uuid
        self.external_id = external_id
        self.program_id = program_id
        self.description = description
        self.created_at = created_at
        self.created_by = created_by
        self.updated_at = updated_at
        self.updated_by = updated_by


class Rqmt_group_rqmt_category(Base):
    # CREATE TABLE `rqmt_group_rqmt_category` (
    #   `id` bigint(20) NOT NULL,
    #   `rqmt_group_id` bigint(20) DEFAULT NULL,
    #   `rqmt_category_id` bigint(20) DEFAULT NULL,
    #   `min_credits` int(11) DEFAULT NULL,
    #   `max_credits` int(11) DEFAULT NULL,
    #   PRIMARY KEY (`id`),
    #   KEY `rqmt_group_rqmt_category_rqmt_group_id` (`rqmt_group_id`),
    #   KEY `rqmt_group_rqmt_category_rqmt_category_id` (`rqmt_category_id`),
    #   CONSTRAINT `rqmt_group_rqmt_category_rqmt_category_id` FOREIGN KEY (`rqmt_category_id`) REFERENCES `rqmt_category` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
    #   CONSTRAINT `rqmt_group_rqmt_category_rqmt_group_id` FOREIGN KEY (`rqmt_group_id`) REFERENCES `rqmt_group` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
    # ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci

    __tablename__ = 'rqmt_group_rqmt_category'
    # uuid = Column('uuid', VARCHAR(75), unique=True, nullable=True)
    rqmt_group_rqmt_category_seq = Sequence('rqmt_group_rqmt_category_seq', increment=1)
    id = Column('id', BigInteger, rqmt_group_rqmt_category_seq, primary_key=True)
    # external_id = Column('external_id', VARCHAR(75), unique=True, nullable=True)
    rqmt_group_id = Column('rqmt_group_id', BigInteger, ForeignKey("rqmt_group.id"))
    rqmt_category_id = Column('rqmt_category_id', BigInteger, ForeignKey("rqmt_category.id"))
    credit_type = Column('credit_type', VARCHAR(75, collation='utf8mb4_unicode_ci'), nullable=True)
    min_credits = Column('min_credits', Float, nullable=True)
    max_credits = Column('max_credits', Float, nullable=True)

    def __init__(self, rqmt_group_id, rqmt_category_id, credit_type, min_credits, max_credits):
        # self.id = id
        self.rqmt_group_id = rqmt_group_id
        self.rqmt_category_id = rqmt_category_id
        self.credit_type = credit_type
        self.min_credits = min_credits
        self.max_credits = max_credits