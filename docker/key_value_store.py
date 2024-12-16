import os
from pathlib import Path

from flask import Flask, jsonify

from dcm_common.db import (
    MemoryStore, JSONFileStore, key_value_store_bp_factory
)


app = Flask(__name__)

if "DB_MOUNT_POINT" in os.environ:
    db_backend = JSONFileStore(Path(os.environ["DB_MOUNT_POINT"]))
else:
    db_backend = MemoryStore()

app.register_blueprint(
    key_value_store_bp_factory(db_backend, "db"),
    url_prefix="/" + os.environ.get("DB_URL_PATH", "")
)


# patch in dumping registry in single call
@app.route("/db-dump", methods=["GET"])
def dump_db():
    """Returns entire registry."""
    result = {}
    for key in db_backend.keys():
        result[key] = db_backend.read(key)
    return jsonify(result), 200
