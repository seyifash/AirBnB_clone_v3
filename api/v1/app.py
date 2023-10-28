#!/usr/bin/python3
""" creating an api"""
from flask import Flask, make_response, jsonify
from models import storage
import os
from api.v1.views import app_views

app = Flask(__name__)

app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_appcontext(error):
    storage.close()


@app.errorhandler(404)
def page_not_found(error):
    """Load 404 page error"""
    return make_response(jsonify({"error": "Not found"}))


if __name__ == "__main__":
    host = os.getenv("HBNB_API_HOST", "0.0.0.0")
    port = int(os.getenv("HBNB_API_PORT", 5000))
    app.run(host=host, port=port, threaded=True)
