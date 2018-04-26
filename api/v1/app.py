*#!/usr/bin/python3
'''
    This Python mode contains the custom-built API for the HBnB project
'''

from models import storage
from api.v1.views import app_views
from flask import Flask
from flask import jsonify
from flask_cors import CORS

app = Flask(__name__)
app.register_blueprint(app_views)
cors = CORS(app, resources={r'/*': {'origins': '0.0.0.0'}})

@app.teardown_appcontext
def teardownContext(exception):
    ''' Ends the session upon execution of this module '''
    storage.close()

@app.errorhandler(404)
def page_not_found(e):
    ''' Returns a 404 page not found error with a custom json page '''
    not_found = jsonify({"error": "Not found"})
    return not_found, 404
    
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
