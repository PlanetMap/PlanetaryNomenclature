from sqlalchemy import create_engine, Column, Integer, String, SmallInteger, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION, REAL
from geoalchemy2 import Geometry
from flask_sqlalchemy import SQLAlchemy
import nomen

NomenDB = SQLAlchemy(nomen.NomenApp)

class Pages(NomenDB.Model):
	__tablename__   = 'pages'
	page_id         = Column(Integer, primary_key=True, autoincrement=True)
	page_name       = Column(String(1024))
	section         = Column(String(1024))
	target_id       = Column(Integer)
	system_id       = Column(Integer)
	content         = Column(String)
	updated_on      = Column(DateTime(timezone=False))

class Features(NomenDB.Model):
    __tablename__       = 'features'
    feature_id          = Column(Integer, primary_key=True, autoincrement=True)
    name                = Column(String(1024), nullable=False)
    clean_name          = Column(String(1024), nullable=False)
    legacy_name         = Column(String(1024))
    ethnicity_id        = Column(Integer)
    feature_type_id     = Column(Integer, nullable=False)
    parent_id           = Column(Integer)
    target_id           = Column(Integer, nullable=False)
    feature_reference_id= Column(Integer)
    description         = Column(String(1024))
    approval_status_id  = Column(Integer)
    approval_date       = Column(DateTime(timezone=False))
    origin              = Column(String(1024))
    updated_on          = Column(DateTime(timezone=False))
    
class Targets(NomenDB.Model):
    __tablename__   = 'targets'
    target_id       = Column(Integer, primary_key=True, autoincrement=True)
    naif_id         = Column(Integer)
    name            = Column(String(20), nullable=False)
    system          = Column(String(20), nullable=False)
    display_name    = Column(String(20))
    a_axis_radius   = Column(DOUBLE_PRECISION)
    b_axis_radius   = Column(DOUBLE_PRECISION)
    c_axis_radius   = Column(DOUBLE_PRECISION)
    description     = Column(String(1024))
    show_map        = Column(Boolean)
    mean_radius     = Column(DOUBLE_PRECISION)
    use_triaxial    = Column(Boolean, default=False)

class Approvalstatuses(NomenDB.Model):
    __tablename__       = 'approvalstatuses'
    approval_status_id  = Column(Integer, primary_key=True, autoincrement=True)
    name                = Column(String(1024))
    short_name          = Column(String(512))

class Continents(NomenDB.Model):
    __tablename__   = 'continents'
    continent_id    = Column(Integer, primary_key=True, autoincrement=True)
    continent_name  = Column(String(1024), nullable=False)
    continent_code  = Column(String(20))

class Controlnets(NomenDB.Model):
    __tablename__   = 'controlnets'
    control_net_id  = Column(Integer, primary_key=True, autoincrement=True)
    name            = Column(String(64), nullable=False)
    target_id       = Column(Integer)
    description     = Column(String(1024))

class Coordinatesystems(NomenDB.Model):
    __tablename__       = 'coordinatesystems'
    coordinate_system_id= Column(Integer, primary_key=True, autoincrement=True)
    name                = Column(String(1024))
    is_planetographic   = Column(Boolean)
    is_positive_east    = Column(Boolean)
    is_0_360            = Column(Boolean)

class Featuregeometries(NomenDB.Model):
    __tablename__       = 'featuregeometries'
    feature_geometry_id = Column(Integer, primary_key=True, autoincrement=True)
    feature_id          = Column(Integer)
    geometry            = Column(Geometry('GEOMETRY'), nullable=False)
    center_point        = Column(Geometry('GEOMETRY'), nullable=False)
    diameter            = Column(REAL, nullable=False)
    control_net_id      = Column(Integer)
    created_on          = Column(DateTime(timezone=False))
    updated_on          = Column(DateTime(timezone=False))
    active              = Column(Boolean)
    northmostlatitude   = Column(DOUBLE_PRECISION) 
    southmostlatitude   = Column(DOUBLE_PRECISION) 
    eastmostlongitude   = Column(DOUBLE_PRECISION) 
    westmostlongitude   = Column(DOUBLE_PRECISION) 

class ethnicitiesd(NomenDB.Model):
    __tablename__   = 'ethnicities'
    ethnicity_id    = Column(Integer, primary_key=True, autoincrement=True)
    continent_id    = Column(Integer, nullable=False)
    ethnicity_name  = Column(String(1024), nullable=False)
    ethnicity_code  = Column(String(20))

class featurereferences(NomenDB.Model):
    __tablename__           = 'featurereferences'
    feature_reference_id    = Column(Integer, primary_key=True, autoincrement=True)
    name                    = Column(String(1024), nullable=False)

class featurerequests(NomenDB.Model):
    __tablename__           = 'featurerequests'
    feature_request_id      = Column(Integer, primary_key=True, autoincrement=True)
    requester_name          = Column(String(1024))
    requester_email         = Column(String(1024))
    requester_affiliation   = Column(String(1024))
    justification           = Column(String)
    additional_info         = Column(String)
    approval_status         = Column(Integer)
    submitted_on            = Column(DateTime(timezone=False))
    updated_on              = Column(DateTime(timezone=False))
    other_reference         = Column(String(1024))
    feature_reference_id    = Column(Integer)
    ethnicity_id            = Column(Integer)
    feature_type_id         = Column(Integer)
    feature_name            = Column(String(1024))
    feature_origin          = Column(String)
    geometry                = Column(Geometry('GEOMETRY'))
    center_point            = Column(Geometry('GEOMETRY'))
    diameter                = Column(REAL)
    target_id               = Column(Integer)
    is_positive_east        = Column(Boolean)

class featuretypes(NomenDB.Model):
    __tablename__   = 'featuretypes'
    feature_type_id = Column(Integer, primary_key=True, autoincrement=True)
    name            = Column(String(1024), nullable=False)
    code            = Column(String(1024))
    description     = Column(String(1024))

class quads(NomenDB.Model):
    __tablename__   = 'quads'
    quad_id         = Column(Integer, primary_key=True, autoincrement=True)
    quad_group_id   = Column(Integer)
    name            = Column(String(1024))
    code            = Column(String(20))
    link            = Column(String(1024))
    geometry        = Column(Geometry('GEOMETRY'))

class targetcoordinates(NomenDB.Model):
    __tablename__           = 'targetcoordinates'
    target_coordinate_id    = Column(Integer, primary_key=True, autoincrement=True)
    target_id               = Column(Integer, nullable=False)
    coordinate_system_id    = Column(Integer, nullable=False)
    accepted_by_the_iau     = Column(Boolean)
    priority                = Column(Integer)

def get_page(name):
    class Page:
        def __init__(self):
            self.title = Pages.query.filter_by(page_name=name.upper(), section='TITLE').first().content
            self.body = Pages.query.filter_by(page_name=name.upper(), section='BODY').first().content
    return Page()