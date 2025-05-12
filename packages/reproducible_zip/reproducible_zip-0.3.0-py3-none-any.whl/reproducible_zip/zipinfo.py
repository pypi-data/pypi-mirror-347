import logging
import shutil

from pathlib import Path
from stat import *
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo


class ReproducibleZipInfo(ZipInfo):
    """Class with readonly attributes for deterministic/repeatable ZIP archive."""

    # properties that must be reproducible
    @property
    def create_system(self) -> int:
        return 3

    @property
    def date_time(self) -> tuple[int]:
        return (1980, 1, 1, 0, 0, 0)

    @property
    def external_attr(self) -> int:
        if self.is_dir():
            return 0x10 | ((S_IFDIR | S_IRWXU | S_IRWXG | S_IRWXO) << 16)
        return (S_IFREG | S_IRWXU | S_IRWXG | S_IRWXO) << 16

    @create_system.setter
    def create_system(self_, value_):
        pass

    @date_time.setter
    def date_time(self_, value_):
        pass

    @external_attr.setter
    def external_attr(self_, value_):
        pass

    def __init__(self, filename="NoName", date_time_=None):
        super().__init__(filename)
        if not self.is_dir():
            self.compress_type = ZIP_DEFLATED


def add_folder_to_zip(
    zf: ZipFile,
    base_dir: str | Path,
    root_dir: str | Path = None,
):
    """Add all files in a directory to a zip file in a reproducible way"""
    root_dir = Path(root_dir or ".")
    base_dir = root_dir / base_dir

    # recurse into base_dir, sorted, with directories first
    paths = sorted(base_dir.rglob("*"), key=lambda _: (0 if _.is_dir() else 1, _))

    for path in paths:
        filename = str(path)
        if path.is_dir():
            filename += "/"
        info = ReproducibleZipInfo(filename=filename)
        zf.writestr(info, path.resolve().read_bytes() if not path.is_dir() else "")


def _make_reproducible_zipfile(
    base_name: str,
    base_dir: str,
    verbose: int = 0,
    dry_run: int = 0,
    logger: logging.Logger = None,
    owner=None,
    group=None,
    root_dir=None,
) -> str:
    """Create a zip file from all the files under 'base_dir'.

    The output zip file will be named 'base_name' + ".zip".  Returns the
    name of the output zip file.
    """
    zip_filename = Path(base_name).with_suffix(".zip")
    with ZipFile(zip_filename, "w", compression=ZIP_DEFLATED) as zf:
        add_folder_to_zip(zf, base_dir, root_dir)
    if root_dir is not None:
        zip_filename = zip_filename.absolute()
    return str(zip_filename)


_make_reproducible_zipfile.supports_root_dir = True
shutil.register_archive_format(
    "reproducible_zip", _make_reproducible_zipfile, [], "Reproducible ZIP file"
)
