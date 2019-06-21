import math
from datetime import datetime
from flask import Flask, Blueprint, render_template, request, Response, redirect, abort
from jinja2 import Markup
from database import (db, PagePart, Feature, Target, ApprovalStatus, Continent, 
	Ethnicity, FeatureReference, FeatureType, FeatureGeometry, CurrentFeature, CoordinateSystem)

router = Blueprint('router', __name__, template_folder='templates')

def yearformat(value, format='%Y'):
	return value.strftime(format)

def dateformat(value, format='%b %d, %Y'):
	return value.strftime(format)

def datetimeformat(value, format='%b %d, %Y %-I:%M %p'):
	return value.strftime(format)

def floatformat(value):
	return '{0:0.2f}'.format(value)

def page_not_found(e):
	return render_template('404.html'), 404

def create_app(config_mode):

	"""
	Nomenclature App Factory / Acceptable Config Modes: 'Dev', 'Test'
	"""
	app = Flask(__name__, instance_relative_config=True)

	try:
		app.config.from_object('config.'+config_mode)
	except:
		print("Configuration not loadable")
	else:
		print(" * {} configuration loaded".format(config_mode))
	
	db.init_app(app)
	app.register_blueprint(router)
	app.register_error_handler(404, page_not_found)
	app.jinja_env.filters['yearformat'] = yearformat
	app.jinja_env.filters['dateformat'] = dateformat
	app.jinja_env.filters['datetimeformat'] = datetimeformat
	app.jinja_env.filters['floatformat'] = floatformat
	return app

@router.route('/', methods = ['GET'])
def home():
	return render_template('home.html', )

@router.route('/Abbreviations', methods = ['GET'])
def abbreviations():
	return render_template('abbreviations.html', abbreviations = Continent.get_all([Continent.continent_name]))

@router.route('/AdvancedSearch', methods=['GET', 'POST'])
def advancedsearch():
	criteria = {}

	if request.method == 'POST':
		criteria = request.form.to_dict()

	return render_template('advancedsearch.html', approved_targets = Target.get_many([Target.features], 
												  									 [Feature.approval_status_id == 5],
																					 [Target.display_name]),
												  feature_types = FeatureType.get_all([FeatureType.name]),
												  continents = Continent.get_all([Continent.continent_name]),												
												  approval_statuses = ApprovalStatus.get_all(),
												  criteria = criteria,
												  feature_references = FeatureReference.get_all([FeatureReference.feature_reference_id]))

@router.route('/DescriptorTerms', methods = ['GET'])
def descriptorterms():
	return render_template('descriptorterms.html', terms = FeatureType.get_all([FeatureType.name]))

@router.route('/Feature/<int:input_feature>', endpoint='feature_id', methods = ['GET'])
@router.route('/Feature/<string:input_feature>', endpoint='feature_name', methods = ['GET'])
def feature(input_feature):
	feature = None
	current_feature = None
	if request.endpoint == 'router.feature_id':
		feature = Feature.get_one([Feature.feature_id == input_feature])
		current_feature = CurrentFeature.get_one([CurrentFeature.feature_id == input_feature])
	elif request.endpoint == 'router.feature_name':
		feature = Feature.get_one([Feature.name == input_feature])
		current_feature = CurrentFeature.get_one([CurrentFeature.name == input_feature])
	else:
		abort(404)

	if feature and current_feature:
		related_content = PagePart.get_page("target", feature.target.name).feature_related
		render_map = feature.target.show_map or (feature.target.target_id == 16 and feature.featuretype.feature_type_id == 52)\
										 	 or (feature.target.target_id == 16 and feature.featuretype.feature_type_id == 9)
		
		return render_template('feature_template.html', feature = feature,
														current_feature = current_feature,
														related_content = Markup(related_content),
														render_map = render_map)
	else:
		abort(404)
	
	# TODO: generate KML from primary attributes (MDIM and CS)
	
@router.route('/GIS_Downloads', methods = ['GET'])
def gisdownloads():
	page = PagePart.get_page("basic", 'GIS_Downloads')
	return render_template('page_template.html', page_title = Markup(page.title),
												 page_body = Markup(page.body),
												 page_javascript = Markup(page.javascript))


@router.route('/FeatureNameRequest', methods = ['GET'])
def namerequest():
	return render_template('featurenamerequest.html', target = Target.get_all([Target.display_name]),
													  feature_types = FeatureType.get_all([FeatureType.name]),
													  continents = Continent.get_all([Continent.continent_name]),
													  ethnicities = Ethnicity.get_all([Ethnicity.ethnicity_name]),
													  feature_references = FeatureReference.get_all([FeatureReference.feature_reference_id]))

@router.route('/References', methods = ['GET'])
def references():
	return render_template('references.html', references = FeatureReference.get_all([FeatureReference.feature_reference_id]))

@router.route('/SearchResults', methods = ['GET', 'POST'])
def searchresults():
	degrees 		  = '(0-360)'
	direction 		  = '+E '
	is_planetographic = False
	is_180			  =	False
	is_positive_west  = False
	
	filters = results = []
	criteria = criteria_labels = {}

	try:

		# parse the search request
		if request.method == 'POST':
			if request.form.get('Feature Name'):
				value = criteria_labels['Feature Name'] = request.form.get('Feature Name')
				filters.append(CurrentFeature.name.ilike(r'%{}%'.format(value)))
			if request.form.get('System'):
				value = criteria_labels['System'] = request.form.get('System')
				filters.append(Target.system.ilike(value))
			if request.form.get('Target'):
				value, criteria_labels['Target'] = request.form.get('Target').split('_')
				filters.append(CurrentFeature.target_id == value)
			if request.form.get('Feature Type'):
				value, criteria_labels['Feature Type'] = request.form.get('Feature Type').split('_')
				filters.append(CurrentFeature.feature_type_id == value)
			if request.form.get('Approval Status'):
				value, criteria_labels['Approval Status'] = request.form.get('Approval Status').split('_')
				filters.append(CurrentFeature.approval_status_id == value)
			if request.form.get('Southernmost Latitude'):
				criteria_labels['Southernmost Latitude'] = request.form.get('Southernmost Latitude')
				filters.append(CurrentFeature.southernmostlatitude >= request.form.get('Southernmost Latitude', type=float))
			if request.form.get('Northernmost Latitude'):
				criteria_labels['Northernmost Latitude'] = request.form.get('Northernmost Latitude')
				filters.append(CurrentFeature.northernmostlatitude <= request.form.get('Southernmost Latitude', type=float))
			if request.form.get('Westernmost Longitude'):
				criteria_labels['Westernmost Longitude'] = request.form.get('Westernmost Longitude')
				filters.append(CurrentFeature.westernmostlongitude <= request.form.get('Westernmost Longitude', type=float))
			if request.form.get('Easternmost Longitude'):
				criteria_labels['Easternmost Longitude'] = request.form.get('Easternmost Longitude')
				filters.append(CurrentFeature.easternmostlongitude <= request.form.get('Easternmost Longitude', type=float))				
			if request.form.get('Minimum Feature Diameter'):
				criteria_labels['Minimum Feature Diameter'] = request.form.get('Minimum Feature Diameter')
				filters.append(CurrentFeature.diameter >= request.form.get('Minimum Feature Diameter', type=float))
			if request.form.get('Maximum Feature Diameter'):
				criteria_labels['Maximum Feature Diameter'] = request.form.get('Maximum Feature Diameter')
				filters.append(CurrentFeature.diameter <= request.form.get('Maximum Feature Diameter', type=float))
			if request.form.get('Beginning Approval Date'):
				label = request.form.get('Beginning Approval Date')
				value = datetime.strptime(label, '%m-%d-%Y')
				criteria_labels['Beginning Approval Date'] = label
				filters.append(CurrentFeature.approval_date >= value)
			if request.form.get('Ending Approval Date'):
				label = request.form.get('Ending Approval Date')
				value = datetime.strptime(label, '%m-%d-%Y')
				criteria_labels['Ending Approval Date'] = label
				filters.append(CurrentFeature.approval_date <= value)
			if request.form.get('Continent'):
				value, criteria_labels['Continent'] = request.form.get('Continent').split('_')
				filters.append(Ethnicity.continent_id == value)
			if request.form.get('Ethnicity'):
				value = request.form.get('Ethnicity')
				criteria_labels['Ethnicity'] = value[2:]
				filters.append(CurrentFeature.ct_ethnicity == value)
			if request.form.get('Reference'):
				value, criteria_labels['Reference'] = request.form.get('Reference').split('_')
				filters.append(CurrentFeature.feature_reference_id == value)
			if request.form.get('Planetographic Latitudes') == 'true':
				is_planetographic = True
				criteria_labels['Planetographic Latitudes'] = 'True'
			if request.form.get('-180 to 180 Degrees') == 'true':
				is_180 = True
				degrees = '(0-180)'
				criteria_labels['-180 to 180 Degrees'] = 'True'
			if request.form.get('Positive West Direction') == 'true':
				is_positive_west = True
				direction = '+W '
				criteria_labels['Positive West Direction'] = 'True'

			criteria = request.form.to_dict()

		if request.method == 'GET':
			value, criteria_labels['Target'] = request.args.get('Target').split('_')
			filters.append(CurrentFeature.target_id == value)

			if request.args.get('Feature Type'):
				value, criteria_labels['Feature Type'] = request.args.get('Feature Type').split('_')
				filters.append(CurrentFeature.feature_type_id == value)
			
			criteria = request.args.to_dict()
	
	except:
		abort(404)
	
	# get search results and project
	if filters:
		results = CurrentFeature.get_many([Target, Ethnicity], filters, [CurrentFeature.name])
		# if one result, redirect to feature page	
		if len(results) == 1:
			return redirect('/Feature/{0}'.format(results[0].name))
	else:
		results = CurrentFeature.get_all([CurrentFeature.name])
	return render_template('searchresults.html', is_planetographic = is_planetographic,
												 is_180 = is_180,
												 is_positive_west = is_positive_west,
												 coordinate_system = direction + degrees,
												 criteria = criteria,
												 criteria_labels = criteria_labels,
												 results = results)

@router.route('/TargetCoordinates', methods = ['GET'])
def targetcoordinates():
	return render_template('targetcoordinates.html', targets = Target.get_many([Feature],
																			   [Feature.approval_status_id == 5],
																			   [Target.display_name]))

@router.route('/Page/<page_name>', methods = ['GET'])
def basicpage(page_name):
	page = PagePart.get_page("basic", page_name)
	return render_template('page_template.html', page_title = Markup(page.title),
												 page_body = Markup(page.body),
												 page_javascript = Markup(page.javascript))

@router.route('/Page/<target_name>/target', methods = ['GET'])
def targetpage(target_name):
	page = PagePart.get_page("target", target_name)
	target = Target.get_one([Target.name == target_name])
	feature_types = FeatureType.get_many([Feature, Target], [Target.name == target_name], [FeatureType.name])
	return render_template('target_template.html', page_title = Markup(page.title),
												   page_body = Markup(page.body),
												   page_javascript = Markup(page.javascript),
												   page_featurerelated = Markup(page.feature_related),
												   page_related = Markup(page.related),
												   target = target,
												   feature_types = feature_types)

@router.route('/Page/<system_name>/system', methods = ['GET'])
def systempage(system_name):
	page = PagePart.get_page("system", system_name)
	return render_template('system_template.html', page_title = Markup(page.title),
												   page_body = Markup(page.body))

if __name__ == "__main__":
	NomenApp = create_app('Dev')
	NomenApp.run(host = '0.0.0.0', port = 5000)