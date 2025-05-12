import shutil
import zipfile


def main(args=None):
    """main() borrowed from python library zipfile.main"""
    import argparse

    description = "A simple command-line interface for reproducible_zip module."
    parser = argparse.ArgumentParser(description=description)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "-l", "--list", metavar="<zipfile>", help="Show listing of a zipfile"
    )
    group.add_argument(
        "-e",
        "--extract",
        nargs=2,
        metavar=("<zipfile>", "<output_dir>"),
        help="Extract zipfile into target dir",
    )
    group.add_argument(
        "-c",
        "--create",
        nargs=2,
        metavar=("<name>", "<base_dir>"),
        help="Create zipfile from source dir",
    )
    group.add_argument(
        "-t", "--test", metavar="<zipfile>", help="Test if a zipfile is valid"
    )
    args = parser.parse_args(args)

    if args.test is not None:
        src = args.test
        with zipfile.ZipFile(src, "r") as zf:
            badfile = zf.testzip()
        if badfile:
            print("The following enclosed file is corrupted: {!r}".format(badfile))
        print("Done testing")

    elif args.list is not None:
        src = args.list
        with zipfile.ZipFile(src, "r") as zf:
            zf.printdir()

    elif args.extract is not None:
        src, curdir = args.extract
        with zipfile.ZipFile(src, "r") as zf:
            zf.extractall(curdir)

    elif args.create is not None:
        zip_name = args.create.pop(0)
        base_dir = args.create[0]
        shutil.make_archive(zip_name, "reproducible_zip", base_dir=base_dir)


if __name__ == "__main__":
    main()
