from flask import Flask, Blueprint, render_template, request, Response
from jinja2 import Markup
from database import (db, PagePart, Feature, Target, ApprovalStatus, Continent,
	Ethnicity, FeatureReference, FeatureType, System)

router = Blueprint('router', __name__, template_folder='templates')

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
	return app

@router.route('/', methods = ['GET'])
def home():
	return render_template('home.html')

@router.route('/Abbreviations', methods = ['GET'])
def abbreviations():
	return render_template('abbreviations.html', abbreviations = Continent.get_all())

@router.route('/AdvancedSearch', methods=['GET'])
def advancedsearch():
	return render_template('advancedsearch.html', systems = System.get_all(),
												approved_targets = Target.get_approved(),
												feature_types = FeatureType.get_all(),
												continents = Continent.get_all(),
												approval_statuses = ApprovalStatus.get_all(),
												feature_references = FeatureReference.get_all())

@router.route('/DescriptorTerms', methods = ['GET'])
def descriptorterms():
	return render_template('descriptorterms.html', terms = FeatureType.get_all())

@router.route('/GIS_Downloads', methods = ['GET'])
def gisdownloads():
	page = PagePart.get_page("basic", 'GIS_Downloads')
	return render_template('page_template.html', page_title = Markup(page.title),
												page_body = Markup(page.body),
												page_javascript = Markup(page.javascript))

@router.route('/Feature/<int:feature_id>')
def feature(feature_id):
	return render_template('page_template.html')

@router.route('/FeatureNameRequest', methods = ['GET'])
def namerequest():
	return render_template('featurenamerequest.html', systems = System.get_all(),
												    target = Target.get_all(),
													feature_types = FeatureType.get_all(),
													continents = Continent.get_all(),
													ethnicities = Ethnicity.get_all(),
													feature_references = FeatureReference.get_all())

@router.route('/References', methods = ['GET'])
def references():
	return render_template('references.html', references = FeatureReference.get_all())

@router.route('/nomenclature/SearchResults', methods = ['GET', 'POST'])
def searchresults():
	# parse the search arguments
	# do the search queries
	# render the page
	return render_template('searchresults.html', page_start = 0,
												result_count = 5,
												results_perpage = 20,
												planetographic = True)

@router.route('/TargetCoordinates', methods = ['GET'])
def targetcoordinates():
	return render_template('targetcoordinates.html', targets = Target.get_approved())

@router.route('/Page/<page_name>', methods = ['GET'])
def basicpage(page_name):
	page = PagePart.get_page("basic", page_name)
	return render_template('page_template.html', page_title = Markup(page.title),
												page_body = Markup(page.body),
												page_javascript = Markup(page.javascript))

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
												feature_types = feature_types)

@router.route('/Page/<system_name>/system', methods = ['GET'])
def systempage(system_name):
	page = PagePart.get_page("system", system_name)
	return render_template('system_template.html', page_title = Markup(page.title),
												page_body = Markup(page.body))


if __name__ == "__main__":
	NomenApp = create_app('Dev')
	NomenApp.run(host = '0.0.0.0', port = 5000)