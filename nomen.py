from flask import Flask, render_template, url_for
from jinja2 import Markup
import database as db

NomenApp = Flask(__name__)
NomenApp.config.from_object('config.TestingConfig')	

@NomenApp.route('/')
def index_handler():
	return render_template('home.html')

@NomenApp.route('/Abbreviations')
def abbrev_handler():
	return render_template('abbreviations.html', abbreviations = db.get_continents())

@NomenApp.route('/AdvancedSearch')
def advancesearch_handler():
	return render_template('advancedsearch.html', 	systems = db.get_systems(),
												  	approved_targets = db.get_approvedtargets(),
												  	feature_types = db.get_featuretypes(),
												 	continents = db.get_continents(),
												 	approval_statuses = db.get_approvalstatuses(),
												 	feature_references = db.get_featurereferences())

@NomenApp.route('/DescriptorTerms')
def descterms_handler():
	return render_template('descriptorterms.html', terms = db.get_featuretypes())

@NomenApp.route('/FeatureNameRequest')
def namerequest_handler():
	return render_template('featurenamerequest.html', 	systems = db.get_systems(),
												      	target = db.get_targets(),
													  	feature_types = db.get_featuretypes(),
													  	continents = db.get_continents(),
													  	ethnicities = db.get_ethnicities(),
													  	feature_references = db.get_featurereferences())

@NomenApp.route('/References')
def ref_handler():
	return render_template('references.html', references = db.get_featurereferences())

@NomenApp.route('/TargetCoordinates')
def targcoorc_handler():
	return render_template('targetcoordinates.html', targets = db.get_approvedtargets())

@NomenApp.route('/Page/<page_name>')
def basicpage_handler(page_name):
	page_title, page_body = db.get_staticpage(page_name)
	return render_template('page_template.html', page_title = Markup(page_title), page_body = Markup(page_body))

@NomenApp.route('/Page/<target_name>/target')
def target_handler(target_name):
	return 'hello'


if __name__ == "__main__":
	db.NomenDB.init_app(NomenApp)
	NomenApp.run(host = '0.0.0.0', port = 5000)