from flask import Flask, render_template
from jinja2 import Markup
import database

NomenApp = Flask(__name__)
NomenApp.config.from_pyfile('config.py')	

@NomenApp.route('/')
def index_handler():
	return render_template('page_template.html', page_title = 'Testing Title', page_body = 'Testing Body')

@NomenApp.route('/Page/<name>')
def page_handler(name):
	page = database.get_page(name)
	return render_template('page_template.html', page_title = Markup(page.title), page_body = Markup(page.body))

if __name__ == "__main__":
	database.NomenDB.init_app(NomenApp)
	NomenApp.run(host = '0.0.0.0', port = 5000, debug=True)

