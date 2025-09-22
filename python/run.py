"""Helper script to start DCM-services in a demo-configuration."""

# pylint: disable=wrong-import-position, wrong-import-order, import-outside-toplevel

import sys
from pathlib import Path

if Path.cwd().resolve() != Path(__file__).parent.resolve():
    print(
        "Please change your current working directory to "
        + f"'{Path(__file__).parent.resolve()}' before running this script.",
        file=sys.stderr,
    )
    sys.exit(1)

# ----------------------------------------------------------------------
# prepare environment
print("Preparing environment..")
# # copy accessory-apps to working directory
import shutil

shutil.copy(Path("../docker/rosetta_stub.py"), Path("rosetta_stub.py"))
shutil.copy(Path("../docker/oaipmh_stub.py"), Path("oaipmh_stub.py"))

# # set up working directory
Path("data/dcm").mkdir(parents=True, exist_ok=True)
Path("data/other").mkdir(parents=True, exist_ok=True)

Path("rosetta_stub_auth").write_bytes(b"Authorization: Basic abc")

# ----------------------------------------------------------------------
# configure services
print("Configuring services..")

from dotenv import load_dotenv


def update_werkzeug_logging(service_name: str, color: str):
    """Replace werkzeug's logging of IP with service name."""
    import logging
    import re

    class ServiceLogFilter(logging.Filter):
        """Filter to prepend service name."""

        pattern: re.Pattern = re.compile(r"^\d+\.\d+\.\d+\.\d+ -")

        def filter(self, record: logging.LogRecord) -> bool:
            record.msg = self.pattern.sub(
                color + service_name + "\033[0m", record.msg
            )
            return True

    logging.getLogger("werkzeug").addFilter(ServiceLogFilter())


services = {}


def create_import_module():
    """Loads env, imports package, and returns flask-app."""
    load_dotenv("env/import_module.env")
    import dcm_import_module

    update_werkzeug_logging("[Import Module]", "\033[0;31m")

    return dcm_import_module.app_factory(
        dcm_import_module.config.AppConfig(), as_process=True
    )


services["Import Module"] = (create_import_module, 8080)


def create_ip_builder():
    """Loads env, imports package, and returns flask-app."""
    load_dotenv("env/ip_builder.env")
    import dcm_ip_builder

    update_werkzeug_logging("[IP Builder]", "\033[0;32m")

    return dcm_ip_builder.app_factory(
        dcm_ip_builder.config.AppConfig(), as_process=True
    )


services["IP Builder"] = (create_ip_builder, 8081)


def create_object_validator():
    """Loads env, imports package, and returns flask-app."""
    load_dotenv("env/object_validator.env")
    import dcm_object_validator

    update_werkzeug_logging("[Object Validator]", "\033[0;33m")

    return dcm_object_validator.app_factory(
        dcm_object_validator.config.AppConfig(), as_process=True
    )


services["Object Validator"] = (create_object_validator, 8082)


def create_preparation_module():
    """Loads env, imports package, and returns flask-app."""
    load_dotenv("env/object_validator.env")
    import dcm_preparation_module

    update_werkzeug_logging("[Preparation Module]", "\033[0;33m")

    return dcm_preparation_module.app_factory(
        dcm_preparation_module.config.AppConfig(), as_process=True
    )


services["Preparation Module"] = (create_preparation_module, 8083)


def create_sip_builder():
    """Loads env, imports package, and returns flask-app."""
    load_dotenv("env/sip_builder.env")
    import dcm_sip_builder

    update_werkzeug_logging("[SIP Builder]", "\033[0;34m")

    return dcm_sip_builder.app_factory(
        dcm_sip_builder.config.AppConfig(), as_process=True
    )


services["SIP Builder"] = (create_sip_builder, 8084)


def create_transfer_module():
    """Loads env, imports package, and returns flask-app."""
    load_dotenv("env/transfer_module.env")
    import dcm_transfer_module

    update_werkzeug_logging("[Transfer Module]", "\033[0;35m")

    return dcm_transfer_module.app_factory(
        dcm_transfer_module.config.AppConfig(), as_process=True
    )


services["Transfer Module"] = (create_transfer_module, 8085)


def create_backend():
    """Loads env, imports package, and returns flask-app."""
    load_dotenv("env/backend.env")
    import dcm_backend

    update_werkzeug_logging("[Backend]", "\033[0;36m")

    config = dcm_backend.config.AppConfig()

    # create directories of hotfolders for the demo
    for hotfolder in config.hotfolders.values():
        hotfolder.mount.mkdir(parents=True, exist_ok=True)

    return dcm_backend.app_factory(config, as_process=True)


services["Backend"] = (create_backend, 8086)


def create_job_processor():
    """Loads env, imports package, and returns flask-app."""
    load_dotenv("env/job_processor.env")
    import dcm_job_processor

    update_werkzeug_logging("[Job Processor]", "\033[1;31m")

    return dcm_job_processor.app_factory(
        dcm_job_processor.config.AppConfig(), as_process=True
    )


services["Job Processor"] = (create_job_processor, 8087)


def create_frontend():
    """Loads env, imports package, and returns flask-app."""
    load_dotenv("env/frontend.env")
    import dcm_frontend

    update_werkzeug_logging("[Frontend]", "\033[2m")

    return dcm_frontend.app_factory(
        dcm_frontend.config.AppConfig()
    )


services["Frontend"] = (create_frontend, 8088)


def create_rosetta_stub():
    """Loads env, imports package, and returns flask-app."""
    load_dotenv("env/rosetta_stub.env")
    from rosetta_stub import app

    update_werkzeug_logging("[Rosetta Stub]", "\033[1;33m")

    return app


services["Rosetta Stub"] = (create_rosetta_stub, 8089)


def create_oaipmh_stub():
    """Loads env, imports package, and returns flask-app."""
    load_dotenv("env/oaipmh_stub.env")
    from oaipmh_stub import app

    update_werkzeug_logging("[OAI-PMH Stub]", "\033[1;34m")

    return app


services["OAI-PMH Stub"] = (create_oaipmh_stub, 8090)

# ----------------------------------------------------------------------
# start services
print("Starting services..")

import multiprocessing
import atexit
from time import sleep

processes = []

omit_list = []
if len(sys.argv) > 1:
    if sys.argv[1].startswith("--omit="):
        omit_list = list(map(
            lambda s: s.lower().strip(),
            " ".join(sys.argv[1:]).replace("--omit=", "", 1).split(","),
        ))


def run_service(s):
    """Run service in separate process."""
    processes.append(
        multiprocessing.Process(
            target=lambda: s[0]().run(host="0.0.0.0", port=s[1], debug=False)
        )
    )
    processes[-1].start()


for p in processes:
    atexit.register(p.kill)

for name, service in services.items():
    if name.lower() in omit_list:
        print(f"* omit {name}..")
        continue
    print(f"* starting {name}..")
    run_service(service)

while True:
    sleep(1)
