DFLAGS=
TAG=
ifeq ($(TAG), )
	_TAG=
else
	_TAG=:${TAG}
endif

_:
	echo "Missing target. See README for details."

import-module:
	docker build -t lzvnrw/import-module${_TAG} -f Dockerfile.import_module ${DFLAGS} .

object-validator:
	docker build -t lzvnrw/object-validator${_TAG} -f Dockerfile.object_validator ${DFLAGS} .

ip-builder:
	docker build -t lzvnrw/ip-builder${_TAG} -f Dockerfile.ip_builder ${DFLAGS} .

preparation-module:
	docker build -t lzvnrw/preparation-module${_TAG} -f Dockerfile.preparation_module ${DFLAGS} .

sip-builder:
	docker build -t lzvnrw/sip-builder${_TAG} -f Dockerfile.sip_builder ${DFLAGS} .

transfer-module:
	docker build -t lzvnrw/transfer-module${_TAG} -f Dockerfile.transfer_module ${DFLAGS} .

job-processor:
	docker build -t lzvnrw/job-processor${_TAG} -f Dockerfile.job_processor ${DFLAGS} .

backend:
	docker build -t lzvnrw/backend${_TAG} -f Dockerfile.backend ${DFLAGS} .

frontend:
	docker build -t lzvnrw/frontend${_TAG} -f Dockerfile.frontend ${DFLAGS} .

queue-registry-notifications:
	docker build -t lzvnrw/queue-registry-notifications${_TAG} -f Dockerfile.queue_registry_notifications ${DFLAGS} .

rosetta-stub:
	docker build -t lzvnrw/rosetta-stub${_TAG} -f Dockerfile.rosetta_stub ${DFLAGS} .

dcm: import-module object-validator ip-builder preparation-module sip-builder transfer-module job-processor backend frontend

all: dcm queue-registry-notifications rosetta-stub
