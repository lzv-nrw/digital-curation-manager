# Digital Curation Manager

This is a meta-repository for the software system `Digital Curation Manager` (DCM) developed in the context of the [LZV.nrw](https://lzv.nrw/)-initiative.

## Repositories
The following is a comprehensive list of related repositories
* APIs
  * [Import Module API](https://github.com/lzv-nrw/dcm-import-module-api)
  * [Object Validator API](https://github.com/lzv-nrw/dcm-object-validator-api)
  * [IP Builder API](https://github.com/lzv-nrw/dcm-ip-builder-api)
  * [SIP Builder API](https://github.com/lzv-nrw/dcm-sip-builder-api)
  * [Transfer Module API](https://github.com/lzv-nrw/dcm-transfer-module-api)
  * [Job Processor API](https://github.com/lzv-nrw/dcm-job-processor-api)
  * [Backend API](https://github.com/lzv-nrw/dcm-backend-api)
* Apps
  * [Import Module](https://github.com/lzv-nrw/dcm-import-module)
  * [Object Validator](https://github.com/lzv-nrw/dcm-object-validator)
  * [IP Builder](https://github.com/lzv-nrw/dcm-ip-builder)
  * [SIP Builder](https://github.com/lzv-nrw/dcm-sip-builder)
  * [Transfer Module](https://github.com/lzv-nrw/dcm-transfer-module)
  * [Job Processor](https://github.com/lzv-nrw/dcm-job-processor)
  * [Backend](https://github.com/lzv-nrw/dcm-backend)
* libraries/other
  * [common](https://github.com/lzv-nrw/dcm-common)
  * [database](https://github.com/lzv-nrw/dcm-database)
  * [s11n](https://github.com/lzv-nrw/dcm-s11n)
  * [metadata-mapper](https://github.com/lzv-nrw/dcm-metadata-mapper)
  * [OAI-PMH-extractor](https://github.com/lzv-nrw/OAI-PMH-extractor)
  * [bag-builder](https://github.com/lzv-nrw/dcm-bag-builder)
  * [bag-validator](https://github.com/lzv-nrw/dcm-bag-validator)

## Install packages locally
To install python-packages associated with this project, [configure `pip`](https://pip.pypa.io/en/stable/cli/pip_install/#finding-packages) to use the extra-index-url `https://zivgitlab.uni-muenster.de/api/v4/projects/9020/packages/pypi/simple`.
This can be achieved, for example, by entering
```
pip install --extra-index-url https://zivgitlab.uni-muenster.de/api/v4/projects/9020/packages/pypi/simple dcm-common
```

## Build docker images
This repository contains `Dockerfile`s for building the images of all dcm-microservices required to run a full (test-)instance of the DCM.
To start the build process, navigate to the `docker/`-directory and run
```
make all
```
for all images used in the [compose-file](#run-with-docker-compose) or
```
make dcm
```
for only the images of dcm-microservices.
The provided `Makefile` also defines targets for all individual images.

Additionally custom flags for the `docker build`-commands can be set via the `DFLAGS`-flag.
To rebuild, e.g., the Import Module-image without using the cache, enter
```
make import-module DFLAGS="--no-cache"
```

### Miscellaneous images
To allow running a comprehensive test-instance, some additional services are required (see target `all` when [building images](#build-docker-images)).
In following, a brief description of the options for environment-configuration are given

#### dcm/key-kalue-store
A simple key-value-store-API for storing JSON-documents that is accessible via HTTP.
* `DB_MOUNT_POINT`: specify the location where JSON-documents should be written; if omitted, an in-memory database-backend is used
* `DB_URL_PATH`: controls the base url-path for the HTTP-API, i.e., the path becomes `/<DB_URL_PATH>`; if omitted, root is used as path

#### dcm/queue-registry-notifications
Combined job queue-, job registry-, and notifications service-solution that is required to scale dcm-microservices horizontally.
* `X_MOUNT_POINT`: where `X` is either `QUEUE` or `REGISTRY`; job queue and registry; see [key-value-store's `DB_MOUNT_POINT`](#dcmkey-kalue-store)
* `NOTIFICATION_REGISTRY`: notification-service user-registry; see [key-value-store's `DB_MOUNT_POINT`](#dcmkey-kalue-store)
* `NOTIFICATION_ABORT_DB`: notification-service abort-subscriptions; see [key-value-store's `DB_MOUNT_POINT`](#dcmkey-kalue-store)

#### dcm/rosetta-stub
Minimal flask app that can be used as a stub for the Rosetta REST-API ([Deposit Web Services](https://developers.exlibrisgroup.com/rosetta/apis/rest-apis/deposits/)).
* `ROSETTA_STUB_OUT`: specify the working directory for the stub-server (used to store temporary files)

## Run with docker compose
The `compose.yml`-file located in the `docker/`-directory can be used for minimal tests or as a starting point for configuring a custom DCM-instance.
To use this configuration, first create a volume with
```
docker volume create dcm_file_storage
```
Then, start up the system by changing into the `docker/`-directory and entering
```
docker compose up
```

The system is configured to use a stub-version as archive system.
By default, only the Backend-service is exposed to the local machine via the port `8085`.
To test whether everything works fine, first post a job configuration to the backend
```
curl -X 'POST' \
  'http://localhost:8085/configure' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "Demo-Config",
  "job": {
    "args": {
      "import_ies": {"import": {"plugin": "demo", "args": {"number": 2, "randomize": true}}},
      "build_ip": {
        "validation": {"modules": []},
        "build": {"configuration": "gASVHRMAAAAAAACMCmRpbGwuX2RpbGyUjAxfY3JlYXRlX3R5cGWUk5QoaACMCl9sb2FkX3R5cGWUk5SMBHR5cGWUhZRSlIwLQnVpbGRDb25maWeUaASMBm9iamVjdJSFlFKUhZR9lCiMCl9fbW9kdWxlX1+UjAhfX21haW5fX5SMCUNPTlZFUlRFUpSMIWx6dm5yd19jb252ZXJ0ZXIub2FpcG1oX2NvbnZlcnRlcpSMF09BSVBNSE1ldGFkYXRhQ29udmVydGVylJOUjAZNQVBQRVKUaAIojANhYmOUjAdBQkNNZXRhlJOUjA5NZXRhZGF0YU1hcHBlcpSMJGRjbV9tZXRhZGF0YV9tYXBwZXIubWFwcGVyX2ludGVyZmFjZZSMD01hcHBlckludGVyZmFjZZSTlIWUfZQoaA6MImRjbV9tZXRhZGF0YV9tYXBwZXIubWFwcGVyX2ZhY3RvcnmUjAdfX2RvY19flIwVTWlhbWkgTWV0YWRhdGEgTWFwcGVylIwMX1NQRUNWRVJTSU9OlChLAEsDSwKMAJR0lIwKTUFQUEVSX1RBR5RoIIwIX19pbml0X1+UaACMEF9jcmVhdGVfZnVuY3Rpb26Uk5QoaACMDF9jcmVhdGVfY29kZZSTlChDHgACBgMIAQYDDAIIAgYBDAIGAwgBCAIGBA4BCgEK/pRLAUsASwBLAksDSxNDfIgCfABfAIgBZAB1AXIUfABqAHIQdAGIAUIAfABfAm4QiAF8AF8Cbgx8AGoAch10AaADoQB8AF8CbgNpAHwAXwKIAGQAdQFyKIgAfABfBG4DaQB8AF8EfABqBKAFoQBEAF0LfQF8AXwAagJ2AHI7fABqAnwBPQBxMGQAUwCUToWUKIwXdXNlX3N0YW5kYXJkX2xpbmVhcl9tYXCUjBNMSU5FQVJfTUFQX1NUQU5EQVJElIwKbGluZWFyX21hcJSMBGNvcHmUjA5fbm9ubGluZWFyX21hcJSMBGtleXOUdJSMBHNlbGaUjANrZXmUhpSMZC9ob21lL3dvcmsvd29ya2luZy9kY20tY2xpL3ZlbnYxMC9saWIvcHl0aG9uMy4xMC9zaXRlLXBhY2thZ2VzL2RjbV9tZXRhZGF0YV9tYXBwZXIvbWFwcGVyX2ZhY3RvcnkucHmUaCVLMkMgBgIIAwYBDAMIAgYCDAEGAggDCAEGAg4ECgEIAQKABP6UaDFoL2gth5QpdJRSlGNkY21fbWV0YWRhdGFfbWFwcGVyLm1hcHBlcl9mYWN0b3J5Cl9fZGljdF9fCmglTmgAjAxfY3JlYXRlX2NlbGyUk5ROhZRSlGg9ToWUUpRoPU6FlFKUh5R0lFKUfZR9lCiMD19fYW5ub3RhdGlvbnNfX5R9lIwGcmV0dXJulE5zjAxfX3F1YWxuYW1lX1+UjD9nZW5lcmF0ZV9tZXRhZGF0YV9tYXBwZXJfY2xhc3MuPGxvY2Fscz4uTWV0YWRhdGFNYXBwZXIuX19pbml0X1+UdYaUYowMZ2V0X21ldGFkYXRhlGgnKGgpKEMaAAYOAgQBBgEC/gQMBPgOAgQBBgEC/gQGBP+USwNLAEsASwRLBEtTQ0h8AaAAoQB8AGoBdgByEXwAoAJ8AaAAoQB8AqECfQN8A1MAfAGgAKEAfABqA3YAciJ8AKAEfAGgAKEAfAKhAn0DfANTAGQAUwCUaCwojAVsb3dlcpRoL4wUX2dldF9tZXRhZGF0YV9saW5lYXKUaDGMF19nZXRfbWV0YWRhdGFfbm9ubGluZWFylHSUKGg0aDWMD3NvdXJjZV9tZXRhZGF0YZSMBXZhbHVllHSUaDdoT0tQQxoOBgQCBgECAQT+BAwO+AQCBgECAQT+BAYE/5QpKXSUUpRjZGNtX21ldGFkYXRhX21hcHBlci5tYXBwZXJfZmFjdG9yeQpfX2RpY3RfXwpoT05OdJRSlH2UfZQoaEl9lChoNWgEjANzdHKUhZRSlGhWjAlfb3BlcmF0b3KUjAdnZXRpdGVtlJOUjAZ0eXBpbmeUjAdNYXBwaW5nlJOUaGNoZ4wKRm9yd2FyZFJlZpSTlCmBlE59lCiMD19fZm9yd2FyZF9hcmdfX5SMHHN0ciB8IGxpc3Rbc3RyXSB8IE5lc3RlZERpY3SUjBBfX2ZvcndhcmRfY29kZV9flGgpKEMAlEsASwBLAEsASwNLQEMQZQBlAWUAGQBCAGUCQgBTAJQpaGGMBGxpc3SUjApOZXN0ZWREaWN0lIeUKYwIPHN0cmluZz6UjAg8bW9kdWxlPpRLAUMCEACUKSl0lFKUjBVfX2ZvcndhcmRfZXZhbHVhdGVkX1+UiYwRX19mb3J3YXJkX3ZhbHVlX1+UTowXX19mb3J3YXJkX2lzX2FyZ3VtZW50X1+UiIwUX19mb3J3YXJkX2lzX2NsYXNzX1+UiYwSX19mb3J3YXJkX21vZHVsZV9flE51hpRihpSGlFKUaEtoZmhnjAVVbmlvbpSTlGhjjAV0eXBlc5SMDEdlbmVyaWNBbGlhc5STlGgEaHOFlFKUaGOFlIaUUpRoBIwITm9uZVR5cGWUhZRSlIeUhpRSlHVoTIxDZ2VuZXJhdGVfbWV0YWRhdGFfbWFwcGVyX2NsYXNzLjxsb2NhbHM+Lk1ldGFkYXRhTWFwcGVyLmdldF9tZXRhZGF0YZR1hpRiaFNoJyhoKShDEgARDgEOAwIBAgEM/gYGDgESApRLA0sASwBLBEsES1NDVmQBfABqAHwBGQB2AHIOfABqAHwBGQBkARkAUwB0AXwCfABqAHwBGQBkAhkAZAONAn0DZAR8AGoAfAEZAHYAcil8AGoAfAEZAGQEGQB8A4MBfQN8A1MAlChYwwEAAAogICAgICAgICAgICBHZXQgdGhlIG1ldGFkYXRhIGJhc2VkIG9uIHRoZSBsaW5lYXIgbWFwLCB3aGljaCBpcyBhIE5lc3RlZERpY3QuCiAgICAgICAgICAgIElmIHRoZSAidmFsdWUiIGtleSBleGlzdHMsIHJldHVybiBpdHMgdmFsdWUuCiAgICAgICAgICAgIE90aGVyd2lzZSwgdXNlIHRoZSB2YWx1ZSBvZiB0aGUgInBhdGgiIGtleSB0byBuYXZpZ2F0ZQogICAgICAgICAgICB0aHJvdWdoIHRoZSBOZXN0ZWREaWN0IG9mIHNvdXJjZV9tZXRhZGF0YSwKICAgICAgICAgICAgZS5nLiwgWyJoZWFkZXIiLCAiaWRlbnRpZmllciJdLgogICAgICAgICAgICBPcHRpb25hbCwgcGVyZm9ybSBwb3N0LXByb2Nlc3NpbmcgYXMgaW5zdHJ1Y3RlZAogICAgICAgICAgICBpbiB0aGUgInBvc3QtcHJvY2VzcyIga2V5LCBlLmcuLCBsYW1iZGEgcHA6IHBwLnJzcGxpdCgiOiIsIDEpWzFdLgogICAgICAgICAgICCUaFeMBHBhdGiUjApuZXN0ZWRkaWN0lGiZhpSMDHBvc3QtcHJvY2Vzc5R0lGgvjBR2YWx1ZV9mcm9tX2RpY3RfcGF0aJSGlChoNIwJa2V5X2xvd2VylGhWaFd0lGg3aFNLZkMSDhEOAQIDAgEMAQb+DgYSAQQClCkpdJRSlGNkY21fbWV0YWRhdGFfbWFwcGVyLm1hcHBlcl9mYWN0b3J5Cl9fZGljdF9fCmhTTk50lFKUfZR9lChoH2iYaEl9lChooGhjaFZog2hLaJN1aEyMS2dlbmVyYXRlX21ldGFkYXRhX21hcHBlcl9jbGFzcy48bG9jYWxzPi5NZXRhZGF0YU1hcHBlci5fZ2V0X21ldGFkYXRhX2xpbmVhcpR1hpRiaFRoJyhoKShDAgAFlEsDSwBLAEsDSwJLU0MOfABqAHwBGQB8AoMBUwCUaCxoMYWUaDRooGhWh5RoN2hUS4ZDAg4FlCkpdJRSlGNkY21fbWV0YWRhdGFfbWFwcGVyLm1hcHBlcl9mYWN0b3J5Cl9fZGljdF9fCmhUTk50lFKUfZR9lChoSX2UKGigaGNoVmiDaEtok3VoTIxOZ2VuZXJhdGVfbWV0YWRhdGFfbWFwcGVyX2NsYXNzLjxsb2NhbHM+Lk1ldGFkYXRhTWFwcGVyLl9nZXRfbWV0YWRhdGFfbm9ubGluZWFylHWGlGKME19fYWJzdHJhY3RtZXRob2RzX1+UKJGUdXSUUpSMCGJ1aWx0aW5zlIwHc2V0YXR0cpSTlGi9aEyMNmdlbmVyYXRlX21ldGFkYXRhX21hcHBlcl9jbGFzcy48bG9jYWxzPi5NZXRhZGF0YU1hcHBlcpSHlFIwaB9OdXSUUpRovowHZ2V0YXR0cpSTlIwEZGlsbJSMBV9kaWxslJOUjAhfc2V0YXR0cpRowIeUUpRoQ4wNY2VsbF9jb250ZW50c5SJh5RSMGjMaEFozX2UKIwYb3JpZ2luLXN5c3RlbS1pZGVudGlmaWVylH2UKGiZXZQojAZoZWFkZXKUjAppZGVudGlmaWVylGVonGgnKGgpKGhxSwFLAEsASwFLBEtDQxx8AGQAdQByBmQAUwB8AKAAZAFkAqECZAMZAFMAlChOjAE6lEsBSwB0lIwGcnNwbGl0lIWUjAJwcJSFlGg3jAg8bGFtYmRhPpRLnUMCHACUKSl0lFKUY2RjbV9tZXRhZGF0YV9tYXBwZXIubWFwcGVyX2ZhY3RvcnkKX19kaWN0X18KaNxOTnSUUpR9lH2UaEl9lHOGlGJ1jBNleHRlcm5hbC1pZGVudGlmaWVylH2UKGiZXZQoaNNo1GVonGgnKGgpKGhxSwFLAEsASwFLBEtDQxx8AGQAdQByBmQAUwB8AKAAZAFkAqECZAIZAFMAlE5o1ksBh5Ro2WjbaDdo3EuhaN0pKXSUUpRjZGNtX21ldGFkYXRhX21hcHBlci5tYXBwZXJfZmFjdG9yeQpfX2RpY3RfXwpo3E5OdJRSlH2UfZRoSX2Uc4aUYnWMCmRjLWNyZWF0b3KUfZRomV2UKIwIbWV0YWRhdGGUjAlvYWlfZGM6ZGOUjApkYzpjcmVhdG9ylGVzjAhkYy10aXRsZZR9lGiZXZQoaPZo94wIZGM6dGl0bGWUZXOMCWRjLXJpZ2h0c5R9lGiZXZQoaPZo94wJZGM6cmlnaHRzlGVzjBNkYy10ZXJtcy1pZGVudGlmaWVylH2UKGiZXZQoaPZo94wNZGM6aWRlbnRpZmllcpRlaJxoJyhoKShDBgwBBgEC/5RLAUsASwBLAUsCS0NDGnwAZAB1AHIGZABTAGQBZAKEAHwARACDAVMAlE5oKShDEAYBAgEMAQIBAgEE/QT/AgGUSwFLAEsASwJLB0tTQyhnAHwAXRB9AXwBZAB1AXICdACgAWQBfAF0AGoCoQNyAnwBkQJxAlMAlE6MJjEwXC5cZHs0LDl9XC9bLS5fOygpLzpBLVowLTldK3x1cm46bmJulIaUjAJyZZSMBnNlYXJjaJSMCklHTk9SRUNBU0WUh5SMAi4wlIwFZW50cnmUhpRoN4wKPGxpc3Rjb21wPpRLr0MSBgACAQwBAgECAQQBBP0C/wYBlCkpdJRSlIwcPGxhbWJkYT4uPGxvY2Fscz4uPGxpc3Rjb21wPpSHlClo22g3aNxLrkMIDAAGAQIBBv+UKSl0lFKUY2RjbV9tZXRhZGF0YV9tYXBwZXIubWFwcGVyX2ZhY3RvcnkKX19kaWN0X18KaNxOTnSUUpR9lH2UaEl9lHOGlGJ1jBNzb3VyY2Utb3JnYW5pemF0aW9ulH2UaFeMH2h0dHBzOi8vZC1uYi5pbmZvL2duZC81MDkxMDMwLTmUc4wNdHJhbnNmZXItdXJsc5R9lChomV2UKGj2jAlvYWlfZGM6ZGOUjA1kYzppZGVudGlmaWVylGWMDHBvc3QtcHJvY2Vzc5RoJyhoKShDBgwBBgEC/5RLAUsASwBLAUsCS0NDGnwAZAB1AHIGZABTAGQBZAKEAHwARACDAVMAlE5oKShDCgYBAgEIAQj+AgKUSwFLAEsASwJLBEtTQyBnAHwAXQx9AXwBZAB1AXIOZAF8AXYAcgJ8AZECcQJTAJROjC5odHRwczovL3JlcG9zaXRvcml1bS51bmktbXVlbnN0ZXIuZGUvdHJhbnNmZXIvlIaUKWoPAQAAjAdlbGVtZW50lIaUjFUvaG9tZS93b3JrL3dvcmtpbmcvZGNtLWNsaS92ZW52MTAvbGliL3B5dGhvbjMuMTAvc2l0ZS1wYWNrYWdlcy9senZucndfbWFwcGVyL21pYW1pLnB5lGoSAQAASxNDDAYAAgEIAQgBAv4GApQpKXSUUpSMHDxsYW1iZGE+Ljxsb2NhbHM+LjxsaXN0Y29tcD6Uh5QpaNqFlGoyAQAAaNxLEkMIDAAGAQIBBv+UKSl0lFKUY2x6dm5yd19tYXBwZXIubWlhbWkKX19kaWN0X18KaNxOTnSUUpR9lH2UaEl9lHOGlGJ1dYeUUjBozGg/aM1Oh5RSMGjAaMRoTGgIh5RSMC4="}
      },
      "ingest": {"ingest": {"archive_identifier": "rosetta"}}
    },
    "from": "import_ies",
    "to": "ingest"
  }
}'
```
If successful, the response contains an identifier that has been assigned to this configuration.
A job-execution can then be triggered by entering
```
curl -X 'POST' \
  'http://localhost:8085/job' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "id": "<id>"
}'
```
A job-token is returned that enables to collect the (current) report-document by
```
curl -X 'GET' \
  'http://localhost:8085/job?token=<token-value>' \
  -H 'accept: application/json'
```
Refer to the [Backend API](https://github.com/lzv-nrw/dcm-backend-api) for more options.

To fully shut down the system, first stop the process and then enter
```
docker compose down
```

# Contributors
* Sven Haubold
* Orestis Kazasidis
* Stephan Lenartz
* Kayhan Ogan
* Michael Rahier
* Steffen Richters-Finger
* Malte Windrath
* Roman Kudinov