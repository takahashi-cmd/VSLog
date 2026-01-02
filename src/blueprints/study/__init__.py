from flask import Blueprint

study_bp = Blueprint('study', __name__)

from .routes import dashboard, fields, graph, logs_list, logs
