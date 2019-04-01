from flask import Flask, render_template, url_for
from jinja2 import Markup
import database

NomenApp = Flask(__name__)
NomenApp.config.from_pyfile('config.py')	

@NomenApp.route('/')
def index_handler():
	return render_template('home.html')

@NomenApp.route('/<page_name>')
def page_handler(page_name):
	if (page_name == 'Abbreviations'):
		return render_template('abbreviations.html', abbreviations = database.get_continents())
	elif (page_name == 'AdvancedSearch'):
		return render_template('advancedsearch.html', systems = database.get_systems(),
													  approvedTargets = database.get_approvedtargets(),
													  feature_types = database.get_featuretypes(),
													  approval_statuses = database.get_approvalstatuses(),
													  continents = database.get_continents(),
													  feature_references = database.get_featurereferences())
	elif (page_name == 'DescriptorTerms'):
		return render_template('descriptorterms.html', terms = database.get_featuretypes())
	elif (page_name == 'References'):
		return render_template('references.html', references = database.get_featurereferences())
	elif (page_name == 'TargetCoordinates'):
		return render_template('targetcoordinates.html', targets = database.get_approvedtargets())
	else:
		return render_template('page_template.html', page_body = '404')

@NomenApp.route('/Page/<page_name>')
def staticpage_handler(page_name):
	page_title, page_body = database.get_staticpage(page_name)
	return render_template('page_template.html', page_title = Markup(page_title), page_body = Markup(page_body))

if __name__ == "__main__":
	database.NomenDB.init_app(NomenApp)
	NomenApp.run(host = '0.0.0.0', port = 5000, debug=True)