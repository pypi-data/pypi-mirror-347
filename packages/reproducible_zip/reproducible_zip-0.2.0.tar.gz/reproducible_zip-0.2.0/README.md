# Reproducible / Deterministic ZipFiles

A tool to generate consistent zip files.

## Installation

```sh
pip install reproducible_zip
```

## Usage

The module uses the same interface as the python builtin `zipfile` module:

```sh
python -m reproducible_zip
```

## How does it work?

There are four tricks to building a deterministic zip:

1) Files must be added to the zip in the same order. `rzip` sorts all directories
   and files (with directories first) before adding them to the zip archive.

2) Files in the zip must have consistent timestamps. The timestamp of files and
   directories is set to the minimum timestamp for zipfiles: 1980-01-01 00:00:00.

3) Files in the zip must have consistent permissions. All permission bits are set
   `-rwxrwxrwx` for files and `drwxrwxrwx` for directories.

4) The "create system" for all files is set to "unix-like" (3) to ensure the correct
   intrepretation of the external_attrs/permissons.


