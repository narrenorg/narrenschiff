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
