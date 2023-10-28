#!/usr/bin/python3
"""Blueprint for API"""
from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

from api.v1.views.index import *
<<<<<<< HEAD
from api.v1.views.cities import *
=======
from api.v1.views.states import *
>>>>>>> 59a334b98bfae0c99fa6c82defa19005825cd87f
