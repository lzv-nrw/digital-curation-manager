DFLAGS =

_:
	echo "Missing target. See README for details."

import-module:
	docker build -t dcm/import-module:latest --secret id=zivgitlab,src=$$HOME/.netrc -f Dockerfile.import_module ${DFLAGS} .

object-validator:
	docker build -t dcm/object-validator:latest --secret id=zivgitlab,src=$$HOME/.netrc -f Dockerfile.object_validator ${DFLAGS} .

ip-builder:
	docker build -t dcm/ip-builder:latest --secret id=zivgitlab,src=$$HOME/.netrc -f Dockerfile.ip_builder ${DFLAGS} .

sip-builder:
	docker build -t dcm/sip-builder:latest --secret id=zivgitlab,src=$$HOME/.netrc -f Dockerfile.sip_builder ${DFLAGS} .

transfer-module:
	docker build -t dcm/transfer-module:latest --secret id=zivgitlab,src=$$HOME/.netrc -f Dockerfile.transfer_module ${DFLAGS} .

job-processor:
	docker build -t dcm/job-processor:latest --secret id=zivgitlab,src=$$HOME/.netrc -f Dockerfile.job_processor ${DFLAGS} .

backend:
	docker build -t dcm/backend:latest --secret id=zivgitlab,src=$$HOME/.netrc -f Dockerfile.backend ${DFLAGS} .

queue-registry-notifications:
	docker build -t dcm/queue-registry-notifications:latest --secret id=zivgitlab,src=$$HOME/.netrc -f Dockerfile.queue_registry_notifications $${DFLAGS} .

key-value-store:
	docker build -t dcm/key-value-store:latest --secret id=zivgitlab,src=$$HOME/.netrc -f Dockerfile.key_value_store ${DFLAGS} .

rosetta-stub:
	docker build -t dcm/rosetta-stub:latest --secret id=zivgitlab,src=$$HOME/.netrc -f Dockerfile.rosetta_stub ${DFLAGS} .

dcm: import-module object-validator ip-builder sip-builder transfer-module job-processor backend

all: dcm queue-registry-notifications key-value-store rosetta-stub
