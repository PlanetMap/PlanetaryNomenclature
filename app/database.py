from datetime import date
from flask_sqlalchemy import SQLAlchemy
from geoalchemy2 import Geometry
from shapely import wkb, wkt
from sqlalchemy import Column, Integer, String, SmallInteger, DateTime, Boolean, ForeignKey, BigInteger, Text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION, REAL

db = SQLAlchemy()

class PagePart(db.Model):
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

class Feature(db.Model):
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
    parentfeature       = relationship('Feature', remote_side=feature_id, backref='childfeatures')

    @hybrid_property
    def clean_approvaldate(self):
        if self.approval_date is not None:
            feature_date = self.approval_date.date()
            if feature_date < date(2006, 9, 13):
                return feature_date.year
            else:
                return feature_date

        return None

    def get_one_byname(name):
        return Feature.query.filter_by(clean_name=name).first()

    def get_one_byid(id):
        return Feature.query.filter_by(feature_id=id).first()
   
class Target(db.Model):
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

    def get_all():
        return Target.query.order_by(Target.display_name).all()

    def get_approved():
        return Target.query.join(Feature)\
                            .filter_by(approval_status_id=5)\
                            .order_by(Target.display_name)\
                            .all()

class ApprovalStatus(db.Model):
    __tablename__       = 'approvalstatuses'
    approval_status_id  = Column(Integer, primary_key=True, autoincrement=True)
    name                = Column(String(1024))
    short_name          = Column(String(512))

    def get_all():
        return ApprovalStatus.query.all()

class Continent(db.Model):
    __tablename__   = 'continents'
    continent_id    = Column(Integer, primary_key=True, autoincrement=True)
    continent_name  = Column(String(1024), nullable=False)
    continent_code  = Column(String(20))
    ethnicities     = relationship('Ethnicity', back_populates='continent')

    def get_all():
        return Continent.query.order_by(Continent.continent_name).all()
    
    def get_one(name):
        return Continent.query.filter_by(continent_name=name).all()

class ControlNet(db.Model):
    __tablename__   = 'controlnets'
    control_net_id  = Column(Integer, primary_key=True, autoincrement=True)
    name            = Column(String(64), nullable=False)
    target_id       = Column(Integer, ForeignKey('targets.target_id'))
    description     = Column(String(1024))
    target          = relationship('Target', back_populates='controlnets')

class CoordinateSystem(db.Model):
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
    controlnet          = relationship('ControlNet')

    @hybrid_property
    def wkb_center(self):
        return wkb.loads(bytes(self.center_point.data))

    @hybrid_property
    def wkb_geometry(self):
        return wkb.loads(bytes(self.center_point.data))

    @hybrid_property
    def wkt_center(self):
        return wkb.loads(bytes(self.center_point.data)).wkt

    @hybrid_property
    def wkt_geometry(self):
        return wkb.loads(bytes(self.geometry.data)).wkt

class Ethnicity(db.Model):
    __tablename__   = 'ethnicities'
    ethnicity_id    = Column(Integer, primary_key=True, autoincrement=True)
    continent_id    = Column(Integer, ForeignKey('continents.continent_id'), nullable=False)
    ethnicity_name  = Column(String(1024), nullable=False)
    ethnicity_code  = Column(String(20))
    continent       = relationship('Continent', back_populates='ethnicities')

    def get_all():
        return Ethnicity.query.order_by(Ethnicity.ethnicity_name).all()

class FeatureReference(db.Model):
    __tablename__           = 'featurereferences'
    feature_reference_id    = Column(Integer, primary_key=True, autoincrement=True)
    name                    = Column(String(1024), nullable=False)

    def get_all():
        return FeatureReference.query.order_by(FeatureReference.feature_reference_id).all()

class FeatureRequest(db.Model):
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

class FeatureType(db.Model):
    __tablename__   = 'featuretypes'
    feature_type_id = Column(Integer, primary_key=True, autoincrement=True)
    name            = Column(String(1024), nullable=False)
    code            = Column(String(1024))
    description     = Column(String(1024))

    def get_all():
        return FeatureType.query.order_by(FeatureType.name).all()

    def get_bytarget(target_name):
        return FeatureType.query.join(Feature)\
                                .join(Target)\
                                .filter_by(name=target_name)\
                                .order_by(FeatureType.name)

class QuadGroup(db.Model):
    __tablename__   = 'quadgroups'
    quad_group_id   = Column(Integer, primary_key=True, autoincrement=True)
    name            = Column(String(1024))
    target_id       = Column(Integer, ForeignKey('targets.target_id'))
    target          = relationship('Target')

class Quad(db.Model):
    __tablename__   = 'quads'
    quad_id         = Column(Integer, primary_key=True, autoincrement=True)
    quad_group_id   = Column(Integer, ForeignKey('quadgroups.quad_group_id'))
    name            = Column(String(1024))
    code            = Column(String(20))
    link            = Column(String(1024))
    geometry        = Column(Geometry('GEOMETRY'))
    quadgroup       = relationship('QuadGroup')           

class TargetCoordinate(db.Model):
    __tablename__           = 'targetcoordinates'
    target_coordinate_id    = Column(Integer, primary_key=True, autoincrement=True)
    target_id               = Column(Integer, ForeignKey('targets.target_id'), nullable=False)
    coordinate_system_id    = Column(Integer, ForeignKey('coordinatesystems.coordinate_system_id'), nullable=False)
    accepted_by_the_iau     = Column(Boolean)
    priority                = Column(Integer)
    target                  = relationship('Target', back_populates='targetcoordinates')
    coordinatesystem        = relationship('CoordinateSystem')

class CurrentFeature(db.Model):
    __tablename__           = 'current_features_view'
    feature_id              = Column(Integer, primary_key=True, nullable=False)
    name                    = Column(String(1024))
    clean_name              = Column(String(1024))
    legacy_name             = Column(String(1024))
    ethnicity_id            = Column(Integer)
    ct_ethnicity            = Column(Text)
    feature_type_id         = Column(Integer)
    parent_id               = Column(Integer)
    target_id               = Column(Integer)
    feature_reference_id    = Column(Integer)
    description             = Column(String(1024))
    approval_status_id      = Column(Integer)
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
    diameter                = Column(REAL)
    control_net_id          = Column(Integer)
    geom_created_on         = Column(DateTime(timezone=False))
    geom_updated_on         = Column(DateTime(timezone=False))
    quad_name               = Column(String(1024))
    quad_code               = Column(String(20))
    quad_link               = Column(String(1024))
    active                  = Boolean

    def get_all():
        return CurrentFeature.query.order_by(clean_name).all()

    def get_one_byid(feature_id):
        return CurrentFeature.query.filter_by(feature_id=feature_id).first()

class System():

    def get_all():
        return Target.query.join(Feature).distinct(Target.system).all()
