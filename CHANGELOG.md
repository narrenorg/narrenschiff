# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [3.4.3] - 2021-09-11
### Fixed
- Security issue `[B506:yaml_load]` (Severity: Medium)

## [3.4.2] - 2021-09-05
### Fixed
- Security issue `[B108:hardcoded_tmp_directory]` (Severity: Medium)

## [3.4.1] - 2021-09-02
### Fixed
- STDOUT gets printed event in the case of error, narrenschiff now defaults to printing STDOUT only if STDERR is missing from shell subprocess
- Test package is not a part of the distribution anymore

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

## [0.6.0] - 2020-05-11
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

[3.4.3]: https://github.com/narrenorg/narrenschiff/compare/3.4.2...3.4.3
[3.4.2]: https://github.com/narrenorg/narrenschiff/compare/3.4.1...3.4.2
[3.4.1]: https://github.com/narrenorg/narrenschiff/compare/3.4.0...3.4.1
[3.4.0]: https://github.com/narrenorg/narrenschiff/releases/tag/3.4.0
[3.3.0]: https://github.com/narrenorg/narrenschiff/compare/982531ae9ebe357e4953adee2e929fd8d9ca3a9c...d6383df0c624910fa2bad57fc5f4974870811998
[3.2.1]: https://github.com/narrenorg/narrenschiff/compare/79c3d7362fe06272393e8530329cfc80e481d16e...982531ae9ebe357e4953adee2e929fd8d9ca3a9c
[3.2.0]: https://github.com/narrenorg/narrenschiff/compare/e3b1926beb32e8fe7f05b07ff1445dfc39198d0c...79c3d7362fe06272393e8530329cfc80e481d16e
[3.1.0]: https://github.com/narrenorg/narrenschiff/compare/211f61bf035d0c3ba391feb8022c5915e8f1685e...e3b1926beb32e8fe7f05b07ff1445dfc39198d0c
[3.0.0]: https://github.com/narrenorg/narrenschiff/compare/7a9b58360619ce4d8eaa11905228211cfa6d2c52...211f61bf035d0c3ba391feb8022c5915e8f1685e
[2.1.0]: https://github.com/narrenorg/narrenschiff/compare/4c5f248b74948c5661d682c9db32706825aec9ce...7a9b58360619ce4d8eaa11905228211cfa6d2c52
[2.0.2]: https://github.com/narrenorg/narrenschiff/compare/119d74421bb3b41f51abef0d121959e4d27ad48f...4c5f248b74948c5661d682c9db32706825aec9ce
[2.0.1]: https://github.com/narrenorg/narrenschiff/compare/dcf870d624296e8dc1bb0dc65e6988e5b4bfa9b4...119d74421bb3b41f51abef0d121959e4d27ad48f
[2.0.0]: https://github.com/narrenorg/narrenschiff/compare/bd4f039b21ee8a217b6d3301f863b8953be5967b...dcf870d624296e8dc1bb0dc65e6988e5b4bfa9b4
[1.6.0]: https://github.com/narrenorg/narrenschiff/compare/0bfa0b26c1a4fb59de909cc7c55835cf7b75c211...bd4f039b21ee8a217b6d3301f863b8953be5967b
[1.5.1]: https://github.com/narrenorg/narrenschiff/compare/d3f141b98fbd4465c83f4763366d9ec1b815ac78...0bfa0b26c1a4fb59de909cc7c55835cf7b75c211
[1.5.0]: https://github.com/narrenorg/narrenschiff/compare/d2591934300c8630cc619df9d657931fec890cd2...d3f141b98fbd4465c83f4763366d9ec1b815ac78
[1.4.0]: https://github.com/narrenorg/narrenschiff/compare/2ddf2c88dbbda7f881e88d5a408f27a9cace5ef1...d2591934300c8630cc619df9d657931fec890cd2
[1.3.0]: https://github.com/narrenorg/narrenschiff/compare/8354bfd0632caa58c76403d081794c119a95fa33...2ddf2c88dbbda7f881e88d5a408f27a9cace5ef1
[1.2.0]: https://github.com/narrenorg/narrenschiff/compare/b646f7bf7f2eaadc1369d90551700527cfd0a703...8354bfd0632caa58c76403d081794c119a95fa33
[1.1.0]: https://github.com/narrenorg/narrenschiff/compare/53a54e4b734306d5dd837ca2e4501ae7578f40e6...b646f7bf7f2eaadc1369d90551700527cfd0a703
[1.0.0]: https://github.com/narrenorg/narrenschiff/compare/051ecc1857aed9213f1b1cbcae2c3ceab99c2f2d...53a54e4b734306d5dd837ca2e4501ae7578f40e6
[0.8.0]: https://github.com/narrenorg/narrenschiff/compare/7bae7d40d5c8c1183d4b4881756695ca8c8f34a0...051ecc1857aed9213f1b1cbcae2c3ceab99c2f2d
[0.7.0]: https://github.com/narrenorg/narrenschiff/compare/c1da599bc8659eb3b0e2b379d0ca13c66b704ede...7bae7d40d5c8c1183d4b4881756695ca8c8f34a0
[0.6.0]: https://github.com/narrenorg/narrenschiff/compare/2038648112b7baa2248430e23d79dc8e11bedb3b...c1da599bc8659eb3b0e2b379d0ca13c66b704ede
[0.5.1]: https://github.com/narrenorg/narrenschiff/compare/7f25c3193ce4b1281b113f30fb36d47e7eb93670...2038648112b7baa2248430e23d79dc8e11bedb3b
[0.5.0]: https://github.com/narrenorg/narrenschiff/compare/e5e45dfa8dd3c65ef417de46ed92a577a78f4e1a...7f25c3193ce4b1281b113f30fb36d47e7eb93670
[0.4.0]: https://github.com/narrenorg/narrenschiff/compare/08b65031761607c926e52093724f7b6fa1cb4261...e5e45dfa8dd3c65ef417de46ed92a577a78f4e1a
[0.3.4]: https://github.com/narrenorg/narrenschiff/compare/c9525d17fb91c3fde0fe1669798e0937d0e0dc47...08b65031761607c926e52093724f7b6fa1cb4261
[0.2.4]: https://github.com/narrenorg/narrenschiff/compare/9aa4d089caa48678c32cec39918f40b9e1af8ae8...c9525d17fb91c3fde0fe1669798e0937d0e0dc47
[0.2.3]: https://github.com/narrenorg/narrenschiff/compare/0d87ba3a93e7ae049454dd56720567900976bd50...9aa4d089caa48678c32cec39918f40b9e1af8ae8
[0.2.2]: https://github.com/narrenorg/narrenschiff/compare/144cefff67a9099cb9d6e227d0dff6e864b19034...0d87ba3a93e7ae049454dd56720567900976bd50
[0.2.1]: https://github.com/narrenorg/narrenschiff/compare/ea9ad431eecf1eb15c3f244ec3257a267766ffdd...144cefff67a9099cb9d6e227d0dff6e864b19034
[0.2.0]: https://github.com/narrenorg/narrenschiff/compare/6de215966e5200107b50d8777ed2587e86d66554...ea9ad431eecf1eb15c3f244ec3257a267766ffdd
[0.1.1]: https://github.com/narrenorg/narrenschiff/compare/77121933edbbdc050ef60d1419679f932e95aa5d...6de215966e5200107b50d8777ed2587e86d66554
[0.1.0]: https://github.com/narrenorg/narrenschiff/compare/4d767450845aaa44435a212e98a542dd99814900...77121933edbbdc050ef60d1419679f932e95aa5d
[0.0.5]: https://github.com/narrenorg/narrenschiff/compare/33527989192bf080b6c56b7696c2a38bb390e248...4d767450845aaa44435a212e98a542dd99814900
[0.0.4]: https://github.com/narrenorg/narrenschiff/compare/72f6a836d20993de4f234a93f05a36dedaa5c907...33527989192bf080b6c56b7696c2a38bb390e248
[0.0.3]: https://github.com/narrenorg/narrenschiff/compare/475e3748bc61199510580361ca82ec09a1872a34...72f6a836d20993de4f234a93f05a36dedaa5c907
[0.0.2]: https://github.com/narrenorg/narrenschiff/commit/475e3748bc61199510580361ca82ec09a1872a34
