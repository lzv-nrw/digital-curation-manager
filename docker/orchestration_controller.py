"""
Definition for a Flask app that serves the orchestra-controller API.
"""

from flask import Flask

from dcm_common.services import OrchestratedAppConfig
from dcm_common.orchestra import get_http_controller_bp


config = OrchestratedAppConfig()

app = Flask("orchestration-controller")

app.register_blueprint(get_http_controller_bp(config.controller))
