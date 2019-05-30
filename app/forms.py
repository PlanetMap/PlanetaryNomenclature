from flask_wtf import FlaskForm
from wtforms import Form, SelectField, SubmitField, BooleanField, StringField
from database import System, Continent, FeatureReference, Target, FeatureType


# submitting this form should have same results as submitting the
# AdvancedSearchForm with just feature_name content entered
class SimpleSearchForm(FlaskForm):
    feature_name    = StringField(id='simple_search_box', render_kw={"alt": "search for a feature by name",
                                                                     "placeholder": "Search by Feature Name..."})
    simple_submit         = SubmitField('Go', id="search_button", render_kw={"alt": "search"})

"""
class AdvancedSearchForm(FlaskForm):
    system = SelectField(u'System:', choices = System.get_all())
    target = SelectField(u'Target:', choices = Target.get_approved())
    is_positive_east = SelectField(label = None, choices = [('true', '+East'),
                                                            ('false', '+West')])
    is_0_360 = SelectField(label = None, choices = [('true', '0 - 360'),
                                                    ('false', '(-180) - 180')])
    is_planetographic = SelectField(label = None, choices = [('false', 'Planetocentric'),
                                                            ('true', 'Planetographic')])
    northmost = StringField()
    southmost = StringField()
    eastmost = StringField()
    westmost = StringField()

    feature_type = SelectField(u'Feature Type:', choices = FeatureType.get_all())
    feature_name = StringFIeld()
    feature_diam = DecimalField()
    approval_date = StringField()
    continent = SelectField(u'Continent:', choices = Continent.get_all())
    ethnicity = SelectField(u'Ethnicity/Cultural Group or Country:', choices = )
    reference = SelectField(u'Reference:', choices = FeatureReference.get_all())
    
    featureid_col = BooleanField()
    featurename_col = BooleanField(default = 'checked')
    cleanfeatname_col = BooleanField()
    target_col = BooleanField(default = 'checked')
    diam_col = BooleanField(default = 'checked')
    centerlatlon_col = BooleanField(default = 'checked')
    latlon_col = BooleanField()
    coordsys_col = BooleanField(default = 'checked')
    conteth_col = BooleanField()
    featuretype_col = BooleanField()
    featuretypecode_col = BooleanField()
    quad_col = BooleanField()
    approvalstatus_col = BooleanField(default = 'checked')
    approvaldate_col = BooleanField(default = 'checked')
    featureref_col = BooleanField()
    origin_col = BooleanField(default = 'checked')
    addinfo_col = BooleanField()
    lastupdated_col = BooleanField()


    sort_by_criteria = SelectField(u'Sort Criteria:', choices = [('name', 'Feature Name'),
                                                                ('feature_id', 'Feature ID'),
                                                                ('diameter', 'Diameter'),
                                                                ('ethnicity', 'Ethnicity'),
                                                                ('featuretype', 'Feature Type'),
                                                                ('quad', 'Quad'),
                                                                ('approvalstatus', 'Approval Status'),
                                                                ('approval_date', 'Approval Date'),
                                                                ('featurereference','Reference'),
                                                                ('updated_on', 'Last Updated')])
    sort_by_order = SelectField(u'Sort Ascending', choices = [('true', 'Ascending'),
                                                            ('false', 'Descending')]
    output = SelectField(u'OutputFormat:', choices = )
    submit =  SubmitField()
"""