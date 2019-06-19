import math
from datetime import date
from flask_sqlalchemy import SQLAlchemy
from geoalchemy2 import Geometry
from geoalchemy2.shape import to_shape
from sqlalchemy import Column, Integer, String, SmallInteger, DateTime, Boolean, ForeignKey, BigInteger, Text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION, REAL

db = SQLAlchemy()

class Base(db.Model):
    __abstract__ = True

    @classmethod
    def get_one(cls, filters=[False]):
        return cls.query.filter(db.and_(*filters)).first()

    @classmethod
    def get_many(cls, joins=[False], filters=[False], orders=[False]):
        return cls.query.outerjoin(*joins)\
                        .filter(db.and_(*filters))\
                        .order_by(*orders).all()

    @classmethod
    def get_all(cls, orders=[False]):
        return cls.query.order_by(*orders).all()
    

class PagePart(Base):
    __tablename__   = 'pages'
    page_id         = Column(Integer, primary_key=True, autoincrement=True)
    page_name       = Column(String(1024))
    section         = Column(String(1024))
    target_id       = Column(Integer, ForeignKey('targets.target_id'))
    system_id       = Column(Integer, ForeignKey('targets.target_id'))
    content         = Column(String)
    updated_on      = Column(DateTime(timezone=False))
    target          = relationship('Target', foreign_keys=[target_id])
    system          = relationship('Target', foreign_keys=[system_id])

    def get_page(page_type, name):
        class Page():
            def __init__(self):
                self.title = ''
                self.body = ''
                self.javascript = ''
                self.feature_related = ''
                self.related = ''

        page = Page()
        page_parts = []

        if page_type == 'basic':
            page_parts = PagePart.query.filter_by(page_name=name.upper()).all()
        elif page_type == 'system':
            page_parts = PagePart.query.join(PagePart.system).filter_by(system=name.upper()).all()
        elif page_type == 'target':
            page_parts = PagePart.query.join(PagePart.target).filter_by(name=name.upper()).all()
        else:
            pass

        if page_parts == []:
            return None
        
        for part in page_parts:
            if part.section == 'TITLE':
                page.title = part.content
            elif part.section == 'BODY':
                page.body = part.content
            elif part.section == 'JAVASCRIPT':
                page.javascript = part.content
            elif part.section == 'FEATURE_RELATED':
                page.feature_related = part.content
            elif part.section == 'RELATED':
                page.related = part.content
            else:
                pass

        return page

class Feature(Base):
    __tablename__       = 'features'
    feature_id          = Column(Integer, primary_key=True, autoincrement=True)
    name                = Column(String(1024), nullable=False)
    clean_name          = Column(String(1024), nullable=False)
    legacy_name         = Column(String(1024))
    ethnicity_id        = Column(Integer, ForeignKey('ethnicities.ethnicity_id'))
    feature_type_id     = Column(Integer, ForeignKey('featuretypes.feature_type_id'), nullable=False)
    parent_id           = Column(Integer, ForeignKey('features.feature_id'))
    target_id           = Column(Integer, ForeignKey('targets.target_id'), nullable=False)
    feature_reference_id= Column(Integer, ForeignKey('featurereferences.feature_reference_id'))
    description         = Column(String(1024))
    approval_status_id  = Column(Integer, ForeignKey('approvalstatuses.approval_status_id'))
    approval_date       = Column(DateTime(timezone=False))
    origin              = Column(String(1024))
    updated_on          = Column(DateTime(timezone=False))
    featuregeometries   = relationship('FeatureGeometry', back_populates='feature')
    ethnicity           = relationship('Ethnicity')
    featuretype         = relationship('FeatureType')
    target              = relationship('Target')
    featurereference    = relationship('FeatureReference')
    approvalstatus      = relationship('ApprovalStatus')
    parentfeature       = relationship('Feature', remote_side=feature_id)
    childfeatures       = relationship('Feature')

    @hybrid_property
    def show_year(self):
        if self.approval_date is None:
            return False
        elif self.approval_date.date() < date(2006, 9, 13):
            return True
        else:
            return False
   
class Target(Base):
    __tablename__       = 'targets'
    target_id           = Column(Integer, primary_key=True, autoincrement=True)
    naif_id             = Column(String(20))
    name                = Column(Integer, nullable=False)
    system              = Column(String(20), nullable=False)
    display_name        = Column(String(20))
    a_axis_radius       = Column(DOUBLE_PRECISION)
    b_axis_radius       = Column(DOUBLE_PRECISION)
    c_axis_radius       = Column(DOUBLE_PRECISION)
    description         = Column(String(1024))
    show_map            = Column(Boolean)
    mean_radius         = Column(DOUBLE_PRECISION)
    use_triaxial        = Column(Boolean, default=False)
    features            = relationship('Feature', back_populates ='target')
    targetcoordinates   = relationship('TargetCoordinate', back_populates='target')
    controlnets         = relationship('ControlNet', back_populates='target')
    currentfeatures     = relationship('CurrentFeature', back_populates = 'target')

class ApprovalStatus(Base):
    __tablename__       = 'approvalstatuses'
    approval_status_id  = Column(Integer, primary_key=True, autoincrement=True)
    name                = Column(String(1024))
    short_name          = Column(String(512))

class Continent(Base):
    __tablename__   = 'continents'
    continent_id    = Column(Integer, primary_key=True, autoincrement=True)
    continent_name  = Column(String(1024), nullable=False)
    continent_code  = Column(String(20))
    ethnicities     = relationship('Ethnicity', back_populates='continent', 
                            order_by="Ethnicity.ethnicity_name")

class ControlNet(Base):
    __tablename__   = 'controlnets'
    control_net_id  = Column(Integer, primary_key=True, autoincrement=True)
    name            = Column(String(64), nullable=False)
    target_id       = Column(Integer, ForeignKey('targets.target_id'))
    description     = Column(String(1024))
    target          = relationship('Target', back_populates='controlnets')

class CoordinateSystem(Base):
    __tablename__       = 'coordinatesystems'
    coordinate_system_id= Column(Integer, primary_key=True, autoincrement=True)
    name                = Column(String(1024))
    is_planetographic   = Column(Boolean)
    is_positive_east    = Column(Boolean)
    is_0_360            = Column(Boolean)

class FeatureGeometry(db.Model):
    __tablename__       = 'featuregeometries'
    feature_geometry_id = Column(Integer, primary_key=True, autoincrement=True)
    feature_id          = Column(Integer, ForeignKey('features.feature_id'))
    geometry            = Column(Geometry('GEOMETRY'), nullable=False)
    center_point        = Column(Geometry('GEOMETRY'), nullable=False)
    diameter            = Column(REAL, nullable=False)
    control_net_id      = Column(Integer, ForeignKey('controlnets.control_net_id'))
    created_on          = Column(DateTime(timezone=False))
    updated_on          = Column(DateTime(timezone=False))
    active              = Column(Boolean)
    northmostlatitude   = Column(DOUBLE_PRECISION) 
    southmostlatitude   = Column(DOUBLE_PRECISION) 
    eastmostlongitude   = Column(DOUBLE_PRECISION) 
    westmostlongitude   = Column(DOUBLE_PRECISION)
    feature             = relationship('Feature', back_populates='featuregeometries')
    #currentfeature      = relationship('CurrentFeature', back_populates='featuregeometry')
    controlnet          = relationship('ControlNet')

    @hybrid_property
    def center_shape(self):
        return to_shape(self.center_point)

    @hybrid_property
    def geometry_shape(self):
        return to_shape(self.geometry)

    @hybrid_property
    def center_wkt(self):
        return (self.center_shape).to_wkt()

    @hybrid_property
    def geometry_wkt(self):
        return (self.geometry_shape).to_wkt()

class Ethnicity(Base):
    __tablename__   = 'ethnicities'
    ethnicity_id    = Column(Integer, primary_key=True, autoincrement=True)
    continent_id    = Column(Integer, ForeignKey('continents.continent_id'), nullable=False)
    ethnicity_name  = Column(String(1024), nullable=False)
    ethnicity_code  = Column(String(20))
    continent       = relationship('Continent', back_populates='ethnicities')

class FeatureReference(Base):
    __tablename__           = 'featurereferences'
    feature_reference_id    = Column(Integer, primary_key=True, autoincrement=True)
    name                    = Column(String(1024), nullable=False)

class FeatureRequest(Base):
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
    feature_reference_id    = Column(Integer, ForeignKey('featurereferences.feature_reference_id'))
    ethnicity_id            = Column(Integer, ForeignKey('ethnicities.ethnicity_id'))
    feature_type_id         = Column(Integer, ForeignKey('featuretypes.feature_type_id'))
    feature_name            = Column(String(1024))
    feature_origin          = Column(String)
    geometry                = Column(Geometry('GEOMETRY'))
    center_point            = Column(Geometry('GEOMETRY'))
    diameter                = Column(REAL)
    target_id               = Column(Integer, ForeignKey('targets.target_id'))
    is_positive_east        = Column(Boolean)
    featurereference        = relationship('FeatureReference')
    ethnicity               = relationship('Ethnicity')
    featuretype             = relationship('FeatureType')
    target                  = relationship('Target')

class FeatureType(Base):
    __tablename__   = 'featuretypes'
    feature_type_id = Column(Integer, primary_key=True, autoincrement=True)
    name            = Column(String(1024), nullable=False)
    code            = Column(String(1024))
    description     = Column(String(1024))

class QuadGroup(Base):
    __tablename__   = 'quadgroups'
    quad_group_id   = Column(Integer, primary_key=True, autoincrement=True)
    name            = Column(String(1024))
    target_id       = Column(Integer, ForeignKey('targets.target_id'))
    target          = relationship('Target')

class Quad(Base):
    __tablename__   = 'quads'
    quad_id         = Column(Integer, primary_key=True, autoincrement=True)
    quad_group_id   = Column(Integer, ForeignKey('quadgroups.quad_group_id'))
    name            = Column(String(1024))
    code            = Column(String(20))
    link            = Column(String(1024))
    geometry        = Column(Geometry('GEOMETRY'))
    quadgroup       = relationship('QuadGroup')           

class TargetCoordinate(Base):
    __tablename__           = 'targetcoordinates'
    target_coordinate_id    = Column(Integer, primary_key=True, autoincrement=True)
    target_id               = Column(Integer, ForeignKey('targets.target_id'), nullable=False)
    coordinate_system_id    = Column(Integer, ForeignKey('coordinatesystems.coordinate_system_id'), nullable=False)
    accepted_by_the_iau     = Column(Boolean)
    priority                = Column(Integer)
    target                  = relationship('Target', back_populates='targetcoordinates')
    coordinatesystem        = relationship('CoordinateSystem')

class CurrentFeature(Base):
    __tablename__           = 'current_features_view'
    feature_id              = Column(Integer, primary_key=True, nullable=False)
    name                    = Column(String(1024))
    clean_name              = Column(String(1024))
    legacy_name             = Column(String(1024))
    ethnicity_id            = Column(Integer, ForeignKey('ethnicities.ethnicity_id'))
    ct_ethnicity            = Column(Text)
    feature_type_id         = Column(Integer, ForeignKey('featuretypes.feature_type_id'))
    parent_id               = Column(Integer)
    target_id               = Column(Integer, ForeignKey('targets.target_id'))
    feature_reference_id    = Column(Integer, ForeignKey('featurereferences.feature_reference_id'))
    description             = Column(String(1024))
    approval_status_id      = Column(Integer, ForeignKey('approvalstatuses.approval_status_id'))
    approval_date           = Column(DateTime(timezone=False))
    origin                  = Column(String(1024))
    feature_updated_on      = Column(DateTime(timezone=False))
    feature_geometry_id     = Column(Integer, nullable=False)
    geometry                = Column(Geometry('GEOMETRY'), nullable=False)
    center_point            = Column(Geometry('GEOMETRY'), nullable=False)
    northmostlatitude       = Column(DOUBLE_PRECISION)
    southmostlatitude       = Column(DOUBLE_PRECISION)
    eastmostlongitude       = Column(DOUBLE_PRECISION)
    westmostlongitude       = Column(DOUBLE_PRECISION)
    diameter                = Column(REAL, nullable=False)
    control_net_id          = Column(Integer)
    geom_created_on         = Column(DateTime(timezone=False))
    geom_updated_on         = Column(DateTime(timezone=False))
    quad_name               = Column(String(1024))
    quad_code               = Column(String(20))
    quad_link               = Column(String(1024))
    active                  = Boolean
    ethnicity               = relationship('Ethnicity')
    featuretype             = relationship('FeatureType')
    target                  = relationship('Target')
    featurereference        = relationship('FeatureReference')
    approvalstatus          = relationship('ApprovalStatus')
    #parentfeature           = relationship('Feature', remote_side=feature_id, backref='childfeatures')
    
    @hybrid_property
    def show_year(self):
        if self.approval_date is None:
            return False
        elif self.approval_date.date() < date(2006, 9, 13):
            return True
        else:
            return False

    @hybrid_property
    def center_shape(self):
        return to_shape(self.center_point)

    @hybrid_property
    def geometry_shape(self):
        return to_shape(self.geometry)

    @hybrid_property
    def center_wkt(self):
        return (self.center_shape).to_wkt()

    @hybrid_property
    def geometry_wkt(self):
        return (self.geometry_shape).to_wkt()
    
    @hybrid_method
    def to_graphic(self, latitude):
        c_axis = self.target.c_axis_radius
        a_axis = self.target.a_axis_radius
        if latitude == None:
            return None
        try:
            new_lat = math.radians(latitude)
            new_lat = math.atan(math.tan(new_lat) * ( c_axis / a_axis ) * ( c_axis / a_axis))
            latitude = math.degrees(new_lat)
        except:
            return latitude
        return latitude

    @hybrid_method
    def to_180(self, longitude):
        if longitude == None:
            return None
        if longitude >= 180.0:
            return longitude - 360.0
        return longitude

    @hybrid_method
    def to_positive_west(self, longitude):
        if longitude == None:
            return None
        return 360.0 - longitude