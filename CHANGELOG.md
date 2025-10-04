
# Change Log
All notable changes to this project will be documented in this file.
 
The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).

## [unreleased]

## [0.5.0] - 2025-10-04

### Changed

- Refactoring: no ad-hoc execution of actions but building an action list
  first, then executing its elements (in an async context). Cleaner
  handling of download / read / write operations. Recognize re-usable wheels
  in the output wheelhouse at an early stage.

- Improved formatting, classifiers, .gitignore and py.typed.

## [0.4.4] - 2025-09-10

### Changed

- Checksum calculation factored out.

- Hopefully better strategy to collect required wheels.

- Some refactoring

### Added

- Report errors and warnings (again) when program run is finished.

## [0.2.0] - 2025-09-01

### Added

- [#1](https://github.com/detlefla/wheel-getter/issues/1)
  Include wheels from editable installations

- [#2](https://github.com/detlefla/wheel-getter/issues/2)
  Use pinned Python version if available

### Fixed

- [#3](https://github.com/detlefla/wheel-getter/issues/3)
  Remove download directory after use

- Excluded editor backup and lock files from wheels / sdists

## [0.1.0] - 2025-09-01
  
Initial release
