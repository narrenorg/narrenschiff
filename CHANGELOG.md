# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [3.4.0] - 2021-08-21

### Added

- License files
- Documentation on Read the Docs

### Changed

- Updated all source code files with the license notice
- Refactor changelog
- Prepare `setup.py` for first public release

## [3.3.0] - 2021-05-18

### Added

- Secretmap now has `diff` subcommand (use it to compare two secretmaps in the same course project)
- New unit tests in order to increase coverage

### Changed

- Refactored kubectl and kustomization module - shared code for dry run is a mixin now

### Fixed

- Delete dead code in Kubectl module (`update_filename_argument` does not need to check if `filename` in `arg` is a list, since `sanitize_filenames` always turns it into a list)
- Bug in `wait_for_pod` module - `cmd` was a reference to deleted method from the parrent, this is fixed now

## [3.2.1] - 2021-01-12

### Fixed

- Delete rendered templates and files from `/tmp/{uuid}` even when program does not exit normally

## [3.2.0] - 2021-01-11

### Added

- Cluster context switching for kubectl (experimental feature)

### Changed

- Add new configuration class that other configuration classes shell reuse by principle of composition

## [3.1.0] - 2020-12-30

### Added

- Dry run is now supported by modules (the implementation works by passing `--dry-run` flag to commands that should be executed)

### Changed

- `get_cmd` abstract method is now `cmd` abstract property (decorator `@property` must be added when inheriting from `NarrenschiffModule`)

### Removed

- Remove unnecessary command attribute from narrenschiff modules

### Fixed

- Remove handling of `CalledProcessError` from `TaskEngine` (errors printing should be handled by task Module echo method)
- Improve UX of `TaskEngine` (remove unnecessary newline after task execution)

## [3.0.0] - 2020-12-24

### Changed

- Gcloud module will fail with commands that require user input, use `--quiet` in opts make these operations pass (**breaking change**)
- Modules are refactored, all subprocess execution is implemented in the parent module
- Execute is now parent module method, and not an abstract method. Instead, `get_cmd` is an abstract method that module needs to override an implement. This method needs to return a command that needs to be executed in a shell

## [2.1.0] - 2020-12-24

### Added

- Enable opts for Kubectl module

### Changed

- Update table formating in documentation (we use list tables instead of regular tables - they are easier to write and maintain)

### Fixed

- Improve UX in case when loading of keys and spices fails
- Improve UX in case when loading of secretmap fails
- Improve UX in case when loading of treasure from secretmap fails
- Remove unnecessary identation in log output

## [2.0.2] - 2020-12-03

### Fixed

- Make sure version appears in METADATA of the packaged tool

## [2.0.1] - 2020-09-14

### Fixed

- Revert changes on missing trailing newline. Secretmaps get alwasy re-encrypted. For the time being, the trailing line is not a problem - it is not obvious which part of the code is removing the original trailing newline - either encryption, or decryption

## [2.0.0] - 2020-08-31

### Fixed

- Add missing trailing newline at the end of the decrypted secretmap
- Renamed `flags` in Gcloud module to `opts` to make Modules API more consistent (**breaking change**)

### Changed

- Updated user and developer documentation

## [1.6.0] - 2020-07-14

### Added

- You can start a project now with `narrenschiff dock`

### Fixed

- Documentation update

## [1.5.1] - 2020-07-09

### Fixed

- Fix includes of course files - imports are now relative to the root of the course project directory

## [1.5.0] - 2020-06-29

### Added

- Basic linter for Jinja2 files - this will linter recursivelly all files within a directory

## [1.4.0] - 2020-06-19

### Added

- You can now check version with `--version` flag
- You can print environment info in case you need this for debugging or issue reporting, this option includes output optionally formatted with Markdown

## [1.3.0] - 2020-06-17

### Added

- Add chest dump option to print all chest values on STDOUT

## [1.2.0] - 2020-06-17

### Added

- You can now search patterns through secretmaps with `search`

## [1.1.0] - 2020-06-10

### Added

- `bash` autocompletion

## [1.0.0] - 2020-05-22

### Changed

- `deploy` is renamed to `sail`

## [0.8.0] - 2020-05-22

### Added

- Becaons - tag a task, if you want to execute only specific set of tasks from the course (use `always` becaon if you want a task executed always regardless of the specified beacons on the command line)

## [0.7.0] - 2020-05-14

### Added

- Better logging in the `Kustomization` module
- Colors for logging

### Changed

- Use magic method (`__getattr__`) to obtain corresponding log level method in the logger class

# 0.6.0 - 11.5.2020.

### Added

- Added `--verbosity` flag on main `narrenschiff` command (it has to be used before any subcommand)
- Added logger class for the tool

## [0.5.1] - 2020-01-30

### Fixed

- Non-edited files by `secretmap alter` command, are not re-encrypted

## [0.5.0] - 2020-01-30

### Added

- User can now delete secretmap file with `narrenschiff secretmap destroy`

## [0.4.0] - 2020-01-30

### Added

- User can now print `secretmap` contentn to `STDOUT` with `peek`

## [0.3.4] - 2019-12-19

### Added

- `gcloud` module now supports flags without arguments

## [0.2.4] - 2019-12-11

### Fixed

- Add `=` to `kubectl` flags in Kubectl module

## [0.2.3] - 2019-12-11

### Fixed

- `name` and `chart` are not any more obligatory when using Helm module

## [0.2.2] - 2019-12-11

### Fixed

- `--name` flag in Helm module replaced with `name` argument

## [0.2.1] - 2019-08-29

### Fixed

- Add support for multiple values in helm install command

## [0.2.0] - 2019-08-29

### Added

- Secretmap can now dynamically edit the file in the preferred editor. The preferred editor on the OS is set with the `EDITOR` environment variable (defaults to `vi`)

## [0.1.1] - 2019-08-27

### Fixed

- Print stack trace when error is encountered

## [0.1.0] - 2019-08-27

### Added

- Secretmap now decrypts and copies files to `/tmp`

### Fixed

- Secretmap file is now storing _relative_ paths

## [0.0.5] - 2019-08-27

### Fixed

- Update `kustomization` module to deploy templated files from the `/tmp`
- Update `kubectl` module to deal with commands without `args`
- Remove dead code from the `TasksEngine`

## [0.0.4] - 2019-08-27

### Fixed

- Secertmap config failing to write filepath when the config file is empty

## [0.0.3] - 2019-08-27

### Fixed

- Added missing implementation of `kustomization` module

## [0.0.2] - 2019-08-27

### Fixed

- Cannot load keys and salts from paths that use `~`
