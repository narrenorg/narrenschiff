# 2.1.0 - 24.12.2020.

## Added

* Enable opts for Kubectl module

## Changed

* Update table formating in documentation (we use list tables instead of regular tables - they are easier to write and maintain)

## Fixed

* Improve UX in case when loading of keys and spices fails
* Improve UX in case when loading of secretmap fails
* Improve UX in case when loading of treasure from secretmap fails
* Remove unnecessary identation in log output

# 2.0.2 - 3.12.2020.

## Fixed

* Make sure version appears in METADATA of the packaged tool

# 2.0.1 - 14.9.2020.

## Fixed

* Revert changes on missing trailing newline. Secretmaps get alwasy re-encrypted. For the time being, the trailing line is not a problem - it is not obvious which part of the code is removing the original trailing newline - either encryption, or decryption

# 2.0.0 - 31.8.2020.

## Fixed

* Add missing trailing newline at the end of the decrypted secretmap
* Renamed `flags` in Gcloud module to `opts` to make Modules API more consistent (**breaking change**)

## Changed

* Updated user and developer documentation

# 1.6.0 - 14.7.2020.

## Added

* You can start a project now with `narrenschiff dock`

## Fixed

* Documentation update

# 1.5.1 - 9.7.2020.

## Fixed

* Fix includes of course files - imports are now relative to the root of the course project directory

# 1.5.0 - 29.6.2020.

## Added

* Basic linter for Jinja2 files - this will linter recursivelly all files within a directory

# 1.4.0 - 19.6.2020.

## Added

* You can now check version with `--version` flag
* You can print environment info in case you need this for debugging or issue reporting, this option includes output optionally formatted with Markdown

# 1.3.0 - 17.6.2020.

## Added

* Add chest dump option to print all chest values on STDOUT

# 1.2.0 - 17.6.2020.

## Added

* You can now search patterns through secretmaps with `search`

# 1.1.0 - 10.6.2020.

## Added

* `bash` autocompletion

# 1.0.0 - 22.5.2020.

## Changed

* `deploy` is renamed to `sail`

# 0.8.0 - 22.5.2020.

## Added

* Becaons - tag a task, if you want to execute only specific set of tasks from the course (use `always` becaon if you want a task executed always regardless of the specified beacons on the command line)

# 0.7.0 - 14.5.2020.

## Added

* Better logging in the `Kustomization` module
* Colors for logging

## Changed

* Use magic method (`__getattr__`) to obtain corresponding log level method in the logger class

# 0.6.0 - 11.5.2020.

## Added

* Added `--verbosity` flag on main `narrenschiff` command (it has to be used before any subcommand)
* Added logger class for the tool

# 0.5.1 - 30.1.2020.

## Fixed

* Non-edited files by `secretmap alter` command, are not re-encrypted

# 0.5.0 - 30.1.2020.

## Added

* User can now delete secretmap file with `narrenschiff secretmap destroy`

# 0.4.0 - 30.1.2020.

## Added

* User can now print `secretmap` contentn to `STDOUT` with `peek`

# 0.3.4 - 19.12.2019.

## Added

* `gcloud` module now supports flags without arguments

# 0.2.4 - 11.12.2019.

## Fixed

* Add `=` to `kubectl` flags in Kubectl module

# 0.2.3 - 11.12.2019.

## Fixed

* `name` and `chart` are not any more obligatory when using Helm module

# 0.2.2 - 11.12.2019.

## Fixed

* `--name` flag in Helm module replaced with `name` argument

# 0.2.1 - 29.8.2019.

## Fixed

* Add support for multiple values in helm install command

# 0.2.0 - 29.8.2019.

## Added

* Secretmap can now dynamically edit the file in the preferred editor. The preferred editor on the OS is set with the `EDITOR` environment variable (defaults to `vi`)

# 0.1.1 - 27.8.2019.

## Fixed

* Print stack trace when error is encountered

# 0.1.0 - 27.8.2019.

## Added

* Secretmap now decrypts and copies files to `/tmp`

## Fixed

* Secretmap file is now storing _relative_ paths

# 0.0.5 - 27.8.2019.

## Fixed

* Update `kustomization` module to deploy templated files from the `/tmp`
* Update `kubectl` module to deal with commands without `args`
* Remove dead code from the `TasksEngine`

# 0.0.4 - 27.8.2019.

## Fixed

* Secertmap config failing to write filepath when the config file is empty

# 0.0.3 - 27.8.2019.

## Fixed

* Added missing implementation of `kustomization` module

# 0.0.2 - 27.8.2019.

## Fixed

* Cannot load keys and salts from paths that use `~`
