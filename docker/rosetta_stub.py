"""
Minimal flask app that can be used as a stub for the Rosetta REST-API
(Deposit Web Services, https://developers.exlibrisgroup.com/rosetta/apis/rest-apis/deposits/).
"""

from typing import Optional
import os
from pathlib import Path
import json
from random import randint
from datetime import datetime

from flask import Flask, jsonify, Response, request


def app_factory(dir_: Optional[Path] = None):
    """
    Returns minimal flask app that can be used to fake responses of the
    Rosetta REST-API calls.
    """
    _app = Flask(__name__)

    if dir_ is not None:
        dir_.mkdir(parents=True, exist_ok=True)

    def create_deposit(subdir, producer, material_flow):
        """Returns deposit-object as dictionary and writes to file."""
        _deposit_id = None
        for _ in range(10):
            __ = str(randint(1000, 9999))
            if not (dir_ / __).exists():
                _deposit_id = __
                break
        if _deposit_id is None:
            return jsonify({}), 500
        date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        deposit = {
            "subdirectory": subdir,
            "id": _deposit_id,
            "creation_date": date,
            "submission_date": date,
            "update_date": date,
            "status": "INPROCESS",
            "title": None,
            "producer_agent": {
                "value": "1234",
                "desc": "Description of the producer agent"
            },
            "producer": {
                "value": producer,
                "desc": "Description of the producer"
            },
            "material_flow": {
                "value": material_flow,
                "desc": "Description of the material flow"
            },
            "sip_id": "101010",
            "sip_reason": None,
            "link": "/rest/v0/deposits/" + _deposit_id
        }
        (dir_ / _deposit_id).write_text(json.dumps(deposit), encoding="utf-8")
        return deposit

    def get_deposit(_deposit_id):
        """
        Tries to load data from working dir and returns appropriate
        response + status code.
        """
        try:
            return (
                jsonify(
                    json.loads(
                        (dir_ / _deposit_id).read_text(encoding="utf-8")
                    )
                ),
                200
            )
        except FileNotFoundError:
            return Response(
                f"Deposit ID {_deposit_id} does not exist.",
                mimetype="text/plain",
                status=204
            )

    @_app.route("/rest/v0/deposits/<id_>", methods=["GET"])
    def deposits_get(id_: str):
        return get_deposit(id_)

    @_app.route("/rest/v0/deposits", methods=["POST"])
    def deposits_post():
        deposit = create_deposit(
            request.json["subdirectory"],
            request.json["producer"]["value"],
            request.json["material_flow"]["value"]
        )
        return jsonify(deposit), 200

    return _app


# this is only relevant for running in docker
try:
    app = app_factory(
        Path(os.environ.get("ROSETTA_STUB_OUT"))
    )
except Exception:
    app = app_factory()
