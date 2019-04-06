from flask import Flask, render_template, url_for
from jinja2 import Markup
import database as db

NomenApp = Flask(__name__)
NomenApp.config.from_object('config.DevelopmentConfig')

#NomenApp = create_app('DevelopmentConfig')

@NomenApp.route('/')
def index_handler():
	return render_template('home.html')

@NomenApp.route('/Abbreviations')
def abbrev_handler():
	return render_template('abbreviations.html', abbreviations = db.Continent.get_all())

@NomenApp.route('/AdvancedSearch')
def advancesearch_handler():
	return render_template('advancedsearch.html', systems = db.System.get_all(),
												approved_targets = db.Target.get_approved(),
												feature_types = db.FeatureType.get_all(),
												continents = db.Continent.get_all(),
												approval_statuses = db.ApprovalStatus.get_all(),
												feature_references = db.get_FeatureReference.get_all())

@NomenApp.route('/DescriptorTerms')
def descterms_handler():
	return render_template('descriptorterms.html', terms = db.FeatureType.get_all())

@NomenApp.route('/FeatureNameRequest')
def namerequest_handler():
	return render_template('featurenamerequest.html', systems = db.System.get_all(),
												    target = db.Target.get_all(),
													feature_types = db.FeatureType.get_all(),
													continents = db.Continent.get_all(),
													ethnicities = db.Ethnicity.get_all(),
													feature_references = db.FeatureReference.get_all())

@NomenApp.route('/References')
def ref_handler():
	return render_template('references.html', references = db.FeatureReference.get_all())

@NomenApp.route('/TargetCoordinates')
def targcoord_handler():
	return render_template('targetcoordinates.html', targets = db.Target.get_approved())

@NomenApp.route('/Page/<page_name>')
def basicpage_handler(page_name):
	page = db.PagePart.get_content_byname(page_name)
	return render_template('page_template.html', page_title = Markup(page.title),
												page_body = Markup(page.body),
												page_javascript = Markup(page.javascript))

@NomenApp.route('/Page/<target_name>/target')
def targetpage_handler(target_name):
	page = db.PagePart.get_content_bytarget(target_name)
	feature_types = db.FeatureType.get_bytarget(target_name)
	return render_template('target_template.html', page_title = Markup(page.title),
												page_body = Markup(page.body),
												page_javascript = Markup(page.javascript),
												page_featurerelated = Markup(page.feature_related),
												page_related = Markup(page.related),
												target_name = target_name,
												feature_types = feature_types)

@NomenApp.route('/Page/<system_name>/system')
def system_handler(system_name):
	return 1


if __name__ == "__main__":
	db.NomenDB.init_app(NomenApp)
	NomenApp.run(host = '0.0.0.0', port = 5000)