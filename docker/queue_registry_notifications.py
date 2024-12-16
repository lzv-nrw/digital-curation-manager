import os
from pathlib import Path

from flask import Flask, jsonify

from dcm_common.db import (
    MemoryStore, JSONFileStore, key_value_store_bp_factory
)
from dcm_common.services.notification import (
    bp_factory as notification_bp_factory, Topic, HTTPMethod
)


app = Flask(__name__)

if "QUEUE_MOUNT_POINT" in os.environ:
    queue_backend = JSONFileStore(Path(os.environ["QUEUE_MOUNT_POINT"]))
else:
    queue_backend = MemoryStore()
if "REGISTRY_MOUNT_POINT" in os.environ:
    registry_backend = JSONFileStore(Path(os.environ["REGISTRY_MOUNT_POINT"]))
else:
    registry_backend = MemoryStore()
if "NOTIFICATION_REGISTRY" in os.environ:
    notification_registry_backend = JSONFileStore(Path(os.environ["NOTIFICATION_REGISTRY"]))
else:
    notification_registry_backend = MemoryStore()
if "NOTIFICATION_ABORT_DB" in os.environ:
    notification_abort_db_backend = JSONFileStore(Path(os.environ["NOTIFICATION_ABORT_DB"]))
else:
    notification_abort_db_backend = MemoryStore()

app.register_blueprint(
    key_value_store_bp_factory(queue_backend, "queue"),
    url_prefix="/queue"
)
app.register_blueprint(
    key_value_store_bp_factory(registry_backend, "registry"),
    url_prefix="/registry"
)
app.register_blueprint(
    notification_bp_factory(
        notification_registry_backend,
        {
            "abort": Topic(
                "", HTTPMethod.DELETE, 200, notification_abort_db_backend
            )
        }, 1.0, os.environ.get("NOTIFICATION_DEBUG_MODE", "0") == "1"
    ),
    url_prefix="/notifications"
)


# patch in dumping registry in single call
@app.route("/registry/db-dump", methods=["GET"])
def dump_db():
    """Returns entire registry."""
    result = {}
    for key in registry_backend.keys():
        result[key] = registry_backend.read(key)
    return jsonify(result), 200
