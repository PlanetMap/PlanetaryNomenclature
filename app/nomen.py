from flask import Flask, Blueprint, render_template, request, Response, redirect, jsonify
from jinja2 import Markup
from database import (db, PagePart, Feature, Target, ApprovalStatus, Continent,
	Ethnicity, FeatureReference, FeatureType, System, FeatureGeometry, CurrentFeature)
from forms import SimpleSearchForm, PagingForm

router = Blueprint('router', __name__, template_folder='templates')

def yearformat(value, format='%Y'):
	return value.strftime(format)

def dateformat(value, format='%b %d, %Y'):
	return value.strftime(format)

def datetimeformat(value, format='%b %d, %Y %-I:%M %p'):
	return value.strftime(format)

def floatformat(value):
	return '{0:0.2f}'.format(value)

def create_app(config_mode):

	"""
	Nomenclature App Factory / Acceptable modes: Acceptable Config Modes: 'Dev', 'Test'
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
	app.jinja_env.filters['yearformat'] = yearformat
	app.jinja_env.filters['dateformat'] = dateformat
	app.jinja_env.filters['datetimeformat'] = datetimeformat
	app.jinja_env.filters['floatformat'] = floatformat
	return app

@router.route('/', methods = ['GET'])
def home():
	return render_template('home.html', simple_search = SimpleSearchForm())


@router.route('/Abbreviations', methods = ['GET'])
def abbreviations():
	return render_template('abbreviations.html', abbreviations = Continent.get_all(), 
												simple_search = SimpleSearchForm())

@router.route('/AdvancedSearch', methods=['GET'])
def advancedsearch():
	return render_template('advancedsearch.html', systems = System.get_all(),
												approved_targets = Target.get_approved(),
												feature_types = FeatureType.get_all(),
												continents = Continent.get_all(),
												approval_statuses = ApprovalStatus.get_all(),
												feature_references = FeatureReference.get_all(),
												simple_search = SimpleSearchForm())

@router.route('/DescriptorTerms', methods = ['GET'])
def descriptorterms():
	return render_template('descriptorterms.html', terms = FeatureType.get_all(),
												simple_search = SimpleSearchForm())

@router.route('/GIS_Downloads', methods = ['GET'])
def gisdownloads():
	page = PagePart.get_page("basic", 'GIS_Downloads')
	return render_template('page_template.html', page_title = Markup(page.title),
												page_body = Markup(page.body),
												page_javascript = Markup(page.javascript),
												simple_search = SimpleSearchForm())

@router.route('/Feature/<int:input_feature>', endpoint='feature_id', methods = ['GET'])
@router.route('/Feature/<string:input_feature>', endpoint='feature_name', methods = ['GET'])
def feature(input_feature):
	feature = None
	current_feature = None
	if request.endpoint == 'router.feature_id':
		feature = Feature.get_one_byid(input_feature)
		current_feature = CurrentFeature.get_one_byid(input_feature)
	elif request.endpoint == 'router.feature_name':
		feature = Feature.get_one_byname(input_feature)
		current_feature = Feature.get_one_byname(input_feature)
	else:
		return render_template('404.html', simple_search = SimpleSearchForm())

	if feature and current_feature:
		related_content = PagePart.get_page("target", feature.target.name).feature_related
		render_map = feature.target.show_map or (feature.target.target_id == 16 and feature.featuretype.feature_type_id == 52)\
										 or (feature.target.target_id == 16 and feature.featuretype.feature_type_id == 9)
		
		return render_template('feature_template.html', feature = feature,
												current_feature = current_feature,
												related_content = Markup(related_content),
												render_map = render_map,
												simple_search = SimpleSearchForm())
	else:
		return render_template('404.html', simple_search = SimpleSearchForm())
	
	# TODO: generate KML from primary attributes (MDIM and CS)
	

@router.route('/FeatureNameRequest', methods = ['GET'])
def namerequest():
	return render_template('featurenamerequest.html', systems = System.get_all(),
												    target = Target.get_all(),
													feature_types = FeatureType.get_all(),
													continents = Continent.get_all(),
													ethnicities = Ethnicity.get_all(),
													feature_references = FeatureReference.get_all(),
													simple_search = SimpleSearchForm())

@router.route('/References', methods = ['GET'])
def references():
	return render_template('references.html', references = FeatureReference.get_all(),
											simple_search = SimpleSearchForm())

@router.route('/SearchResults', methods = ['GET', 'POST'])
def searchresults():
	default_cs = 'planetocentric'
	criteria = {}
	results = []

	if request.method == 'POST':
		# if a simple search
		if 'simple_submit' in request.form:
			#criteria['feature_name'] = request.form.get('feature_name')
			results = CurrentFeature.get_all_likename(request.form.get('feature_name'))

		# if an advanced search
		if 'advanced_submit' in request.form:
			results = CurrentFeature.get_all_likename(request.form.get('feature_name'))
	
	# if exactly one result, redirect to feature page	
	if len(results) == 1:
		feature = results[0]
		return redirect('/Feature/{0}'.format(feature.name))

	# otherwise, load search results
	else:
		return render_template('searchresults.html',default_cs = default_cs,
													criteria = criteria,
													results = results,
													simple_search = SimpleSearchForm())

@router.route('/TargetCoordinates', methods = ['GET'])
def targetcoordinates():
	return render_template('targetcoordinates.html', targets = Target.get_approved(),
													simple_search = SimpleSearchForm())

@router.route('/Page/<page_name>', methods = ['GET'])
def basicpage(page_name):
	page = PagePart.get_page("basic", page_name)
	return render_template('page_template.html', page_title = Markup(page.title),
												page_body = Markup(page.body),
												page_javascript = Markup(page.javascript),
												simple_search = SimpleSearchForm())

@router.route('/Page/<target_name>/target', methods = ['GET'])
def targetpage(target_name):
	page = PagePart.get_page("target", target_name)
	feature_types = FeatureType.get_bytarget(target_name)
	return render_template('target_template.html', page_title = Markup(page.title),
												page_body = Markup(page.body),
												page_javascript = Markup(page.javascript),
												page_featurerelated = Markup(page.feature_related),
												page_related = Markup(page.related),
												target_name = target_name,
												feature_types = feature_types,
												simple_search = SimpleSearchForm())

@router.route('/Page/<system_name>/system', methods = ['GET'])
def systempage(system_name):
	page = PagePart.get_page("system", system_name)
	return render_template('system_template.html', page_title = Markup(page.title),
												page_body = Markup(page.body),
												simple_search = SimpleSearchForm())


if __name__ == "__main__":
	NomenApp = create_app('Dev')
	NomenApp.run(host = '0.0.0.0', port = 5000)