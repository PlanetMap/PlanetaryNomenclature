from sqlalchemy import create_engine, Column, Integer, String, SmallInteger, DateTime, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION, REAL
from geoalchemy2 import Geometry
from flask_sqlalchemy import SQLAlchemy
import nomen

NomenDB = SQLAlchemy(nomen.NomenApp)

class PagePart(NomenDB.Model):
    __tablename__   = 'pages'
    page_id         = Column(Integer, primary_key=True, autoincrement=True)
    page_name       = Column(String(1024))
    section         = Column(String(1024))
    target_id       = Column(Integer, ForeignKey('targets.target_id'))
    system_id       = Column(Integer)
    content         = Column(String)
    updated_on      = Column(DateTime(timezone=False))
    target          = relationship('Target', back_populates='page_parts')

    def get_content_byname(page_name):
        class BasicPage():
            def __init__(self):
                self.title = ''
                self.body = ''
                self.javascript = ''
        
        page_parts = PagePart.query.filter_by(page_name=page_name.upper()).all()
        page = BasicPage()

        for part in page_parts:
            if part.section == 'TITLE':
                page.title = part.content
            elif part.section == 'BODY':
                page.body = part.content
            elif part.section == 'JAVASCRIPT':
                page.javascript = part.content
            else:
                pass

        return page

    def get_content_bysystem(system_name):
        class SystemPage():
            def __init__(self):
                self.title = ''
                self.body = ''

        page_parts = PagePart.query.filter_by(system_id=system)
        page = SystemPage()
        
        for part in page_parts:
            if part.section == 'TITLE':
                page.title = part.content
            elif part.section == 'BODY':
                page.body = part.content
            else:
                pass

        return page

    def get_content_bytarget(target_name):
        class TargetPage():
            def __init__(self):
                self.title = ''
                self.body = ''
                self.javascript = ''
                self.feature_related = ''
                self.related = ''

        target = Target.query.filter_by(name=target_name.upper()).first()       
        page = TargetPage()

        for part in target.page_parts:
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

class Feature(NomenDB.Model):
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
    parentfeature       = relationship('Feature', remote_side=feature_id, backref='sub_features')
    

class Target(NomenDB.Model):
    __tablename__       = 'targets'
    target_id           = Column(Integer, primary_key=True, autoincrement=True)
    naif_id             = Column(Integer)
    name                = Column(String(20), nullable=False)
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
    page_parts          = relationship('PagePart', back_populates='target')

    def get_all():
        return Target.query.order_by(Target.display_name)

    def get_approved():
        return Target.query.join(Feature).order_by(Target.display_name)

class ApprovalStatus(NomenDB.Model):
    __tablename__       = 'approvalstatuses'
    approval_status_id  = Column(Integer, primary_key=True, autoincrement=True)
    name                = Column(String(1024))
    short_name          = Column(String(512))

    def get_all():
        return ApprovalStatus.query.all()

class Continent(NomenDB.Model):
    __tablename__   = 'continents'
    continent_id    = Column(Integer, primary_key=True, autoincrement=True)
    continent_name  = Column(String(1024), nullable=False)
    continent_code  = Column(String(20))
    ethnicities     = relationship('Ethnicity', back_populates='continent')

    def get_all():
        return Continent.query.order_by(Continent.continent_name)

class ControlNet(NomenDB.Model):
    __tablename__   = 'controlnets'
    control_net_id  = Column(Integer, primary_key=True, autoincrement=True)
    name            = Column(String(64), nullable=False)
    target_id       = Column(Integer, ForeignKey('targets.target_id'))
    description     = Column(String(1024))
    target          = relationship('Target', back_populates='controlnets')

class CoordinateSystem(NomenDB.Model):
    __tablename__       = 'coordinatesystems'
    coordinate_system_id= Column(Integer, primary_key=True, autoincrement=True)
    name                = Column(String(1024))
    is_planetographic   = Column(Boolean)
    is_positive_east    = Column(Boolean)
    is_0_360            = Column(Boolean)

class FeatureGeometry(NomenDB.Model):
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

class Ethnicity(NomenDB.Model):
    __tablename__   = 'ethnicities'
    ethnicity_id    = Column(Integer, primary_key=True, autoincrement=True)
    continent_id    = Column(Integer, ForeignKey('continents.continent_id'), nullable=False)
    ethnicity_name  = Column(String(1024), nullable=False)
    ethnicity_code  = Column(String(20))
    continent       = relationship('Continent', back_populates='ethnicities')

    def get_all():
        return Ethnicity.query.order_by(Ethnicity.ethnicity_name)

class FeatureReference(NomenDB.Model):
    __tablename__           = 'featurereferences'
    feature_reference_id    = Column(Integer, primary_key=True, autoincrement=True)
    name                    = Column(String(1024), nullable=False)

    def get_all():
        return FeatureReference.query.order_by(FeatureReference.feature_reference_id)

class FeatureRequest(NomenDB.Model):
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

class FeatureType(NomenDB.Model):
    __tablename__   = 'featuretypes'
    feature_type_id = Column(Integer, primary_key=True, autoincrement=True)
    name            = Column(String(1024), nullable=False)
    code            = Column(String(1024))
    description     = Column(String(1024))

    def get_all():
        return FeatureType.query.order_by(FeatureType.name)

    def get_bytarget(target_name):
        return FeatureType.query.join(Feature)\
                                .join(Target)\
                                .filter_by(name=target_name)\
                                .order_by(FeatureType.name)

class Quad(NomenDB.Model):
    __tablename__   = 'quads'
    quad_id         = Column(Integer, primary_key=True, autoincrement=True)
    quad_group_id   = Column(Integer)
    name            = Column(String(1024))
    code            = Column(String(20))
    link            = Column(String(1024))
    geometry        = Column(Geometry('GEOMETRY'))

class TargetCoordinate(NomenDB.Model):
    __tablename__           = 'targetcoordinates'
    target_coordinate_id    = Column(Integer, primary_key=True, autoincrement=True)
    target_id               = Column(Integer, ForeignKey('targets.target_id'), nullable=False)
    coordinate_system_id    = Column(Integer, ForeignKey('coordinatesystems.coordinate_system_id'), nullable=False)
    accepted_by_the_iau     = Column(Boolean)
    priority                = Column(Integer)
    target                  = relationship('Target', back_populates='targetcoordinates')
    coordinatesystem        = relationship('CoordinateSystem')

class System():
    def get_all():
        return Target.query.join(Feature).distinct(Target.system)







#def get_staticpage(page_name):
#    page_title = PagePart.query.filter_by(page_name=page_name.upper(), section='TITLE').first()
#    page_body = PagePart.query.filter_by(page_name=page_name.upper(), section='BODY').first()
#    return page_title.content, page_body.content

## relationship loading techniques? -- joined eager loading
## how is sqlalchemy generating individual statements? (repeated selects vs. joins, etc.)
#def get_continents():
#    return Continent.query.order_by(Continent.continent_name)

#def get_featurereferences():
#    return FeatureReference.query.order_by(FeatureReference.feature_reference_id).all()

# check-in about results
#def get_approvedtargets():
#    return Target.query.join(Feature).order_by(Target.display_name).all()

#def get_targets():
#    return Target.query.order_by(Target.display_name)

#def get_featuretypes():
#    return FeatureType.query.order_by(FeatureType.name)

#def get_approvalstatuses():
#    return ApprovalStatus.query.all()

#def get_systems():
#    return Target.query.join(Feature).distinct(Target.system)

#def get_ethnicities():
#    return Ethnicity.query.order_by(Ethnicity.ethnicity_name)





