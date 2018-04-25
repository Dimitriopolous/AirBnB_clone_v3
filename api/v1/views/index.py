from api.v1.views import app_views
from flask import jsonify
from models import classes, storage

@app_views.route('/status', strict_slashes=False)
def returnStatus():
    ''' return a JSON object with the given key and value '''
    return jsonify({"status": "OK"})

@app_views.route('/stats', strict_slashes=False)
def retrieveNumbers():
    ''' retrieves the number of each object by type '''
    counting_dict = {}
    for key, value in classes.items():
        if key != "BaseModel":
            counting_dict[key] = storage.count(key)
    return jsonify(counting_dict)
