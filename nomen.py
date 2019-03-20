from flask import Flask, render_template
# import nomenDB

app = Flask(__name__)


@app.route('/')
def index_handler():
	return render_template('page_template.html')

if __name__ == "__main__":
	app.run(host = '0.0.0.0', port = 5000, debug=True)
