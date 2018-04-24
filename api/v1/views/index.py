from api.v1.views import app_views

@app.route('/status')
def returnStatus(self):
    return {"status": "OK")
