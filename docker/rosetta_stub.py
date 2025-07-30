"""
Minimal flask app that can be used as a stub for the Rosetta REST-API
* (Deposit Web Services, https://developers.exlibrisgroup.com/rosetta/apis/rest-apis/deposits/).
* (SIP Processing Related Web Services, https://developers.exlibrisgroup.com/rosetta/apis/rest-apis/sips/).
"""

from typing import Optional
import os
from pathlib import Path
import json
import datetime
from random import choices

from flask import Flask, jsonify, request


def app_factory(dir_: Optional[Path] = None):
    """
    Returns Rosetta-REST API v0-stub.

    If no `_dir` is passed, run in-memory, otherwise on disk in given
    directory.

    NOTE: On update, please consider also updating the stub in
    'dcm-backend' accordingly.
    """
    _app = Flask(__name__)

    deposit_dir = None
    sip_dir = None
    deposit_cache = None
    sip_cache = None
    mem = dir_ is None
    if mem:
        deposit_cache = {}
        sip_cache = {}
    else:
        deposit_dir = dir_ / "deposit"
        sip_dir = dir_ / "sip"

    def create_deposit(subdirectory, producer, material_flow):
        """
        Returns deposit-object as dictionary and writes deposit+sip
        to caches/files.
        """
        deposit_id = None
        for _ in range(10):
            __ = "".join(choices("0123456789", k=4))
            if (dir_ is None and __ not in deposit_cache) or (
                dir_ is not None and not (dir_ / __).exists()
            ):
                deposit_id = __
                break
        if deposit_id is None:
            return jsonify({}), 500
        sip_id = f"SIP{deposit_id}"
        date = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        deposit = {
            "subdirectory": subdirectory,
            "id": deposit_id,
            "creation_date": date,
            "submission_date": date,
            "update_date": date,
            "status": "INPROCESS",  # REJECTED, DECLINED, INPROCESS, FINISHED, DELETED, ERROR, IN_HUMAN_STAGE
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
            "sip_id": sip_id,
            "sip_reason": None,
            "link": "/rest/v0/deposits/" + deposit_id
        }
        sip = {
            "link": "/rest/v0/sips/" + sip_id,
            "id": f"SIP{deposit_id}",
            "externalId": None,
            "externalSystem": None,
            "stage": "Deposit",  # Deposit, Loading, Validation, Assessor, Arranger, Approver, Bytestream, Enrichment, ToPermanent, Finished
            "status": "INPROCESS",  # REJECTED, DECLINED, INPROCESS, FINISHED, DELETED, ERROR, IN_HUMAN_STAGE
            "numberofIEs": "1",
            "iePids": f"IE{deposit_id}",
        }
        if mem:
            deposit_cache[deposit_id] = deposit
            sip_cache[sip_id] = sip
        else:
            deposit_dir.mkdir(parents=True, exist_ok=True)
            sip_dir.mkdir(parents=True, exist_ok=True)
            (deposit_dir / deposit_id).write_text(
                json.dumps(deposit), encoding="utf-8"
            )
            (sip_dir / sip_id).write_text(
                json.dumps(sip), encoding="utf-8"
            )
        return deposit

    def get_deposit(deposit_id):
        """
        Returns deposit data from cache/disk or `None` if
        unavailable.
        """
        result = None
        if mem:
            result = deposit_cache.get(deposit_id)
        else:
            if (deposit_dir / deposit_id).is_file():
                result = json.loads(
                    (deposit_dir / deposit_id).read_text(encoding="utf-8")
                )
        return result

    def get_sip(sip_id):
        """
        Tries to load data from working dir and returns appropriate
        response + status code.
        """
        result = None
        if mem:
            result = sip_cache.get(sip_id)
        else:
            if (sip_dir / sip_id).is_file():
                result = json.loads(
                    (sip_dir / sip_id).read_text(encoding="utf-8")
                )
        if result is None:
            # for some reason requesting a non-existent SIP returns
            # this object
            return {
                "link": None,
                "id": None,
                "externalId": None,
                "externalSystem": None,
                "stage": None,
                "status": None,
                "numberofIEs": None,
                "iePids": None,
            }
        return result

    @_app.route("/rest/v0/deposits/<id_>", methods=["GET"])
    def deposits_get(id_: str):
        data = get_deposit(id_)
        if data is None:
            return jsonify(None), 204
        return jsonify(data), 200

    @_app.route("/rest/v0/sips/<id_>", methods=["GET"])
    def sips_get(id_: str):
        data = get_sip(id_)
        if data is None:
            return jsonify(None), 204
        return jsonify(data), 200

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
