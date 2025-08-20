# Changelog

## [2025.08.0] - 2025-08-20

### Changed

- updated package versions
- updated snapshots of frontend client

### Added

- added snapshot of software-architecture to README

## [2025.07.0] - 2025-07-30

### Changed

- switch to configuration via ENV-files
- changed Backend default port
- changed Docker image namespace from `dcm` to `lzvnrw`
- changed bound port in Dockerfiles from 80 to 8080
- migrated to Backend v3
- migrated to Job Processor v2
- migrated to Import Module v4
- migrated to IP Builder v6
- migrated to Object Validator v5
- pinned JHOVE-version in Object Validator-Dockerfile
- added build-information to compose-file
- updated Dockerfiles to allow running as non-root

### Added

- added frontend and preparation module to demo-configuration
- added 'SIP Processing Related Web Services' to rosetta stub
- added initial `dcm-preparatiob-module`-Dockerfile
- added `python3` starter script for sample-configurations
- added initial `dcm-frontend`-Dockerfile
- added build-arg `BUILD_VERSION_SELECTOR` to Dockerfiles
- added checksum-validation for JHOVE in Object Validator-Dockerfile

## [2024.12.1] - 2024-12-18

### Fixed

- removed obsolete mounting of secrets in Makefile

## [2024.12.0] - 2024-12-12

### Changed

- initial release of `digital-curation-manger`
