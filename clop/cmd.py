import os
import sys
import argparse
import tempfile
import subprocess
from clop import __version__
from clop.translate import translate_file

def translate(args):
    if args.o:
        with open(args.o, "w") as fp:
            translate_file(args.file[0], fp)
    else:
        translate_file(args.file[0])

def run(args):
    fname = args.file[0]
    cc = args.cc[0]
    cwd = os.path.abspath("./")
    with tempfile.TemporaryDirectory(prefix="clop-run", dir=cwd) as dstdir:
        cfname = os.path.join(dstdir, "a.c")
        with open(cfname, "w") as fp:
            translate_file(fname, fp)
        os.chdir(dstdir)
        cmd = [cc, "a.c", "-o", "clop-run.out"]
        subprocess.check_output(cmd)
        subprocess.check_call(["./clop-run.out"])

parser = argparse.ArgumentParser(usage="%(prog)s [-h|-v] [command] [options] file")
parser.add_argument("-v", "--version",
                    action="store_true",
                    help="show version info and exit")

subparsers = parser.add_subparsers(prog=parser.prog,
                                   title="commands",
                                   metavar="run, translate")

parser_translate = subparsers.add_parser("translate",
                                         usage="%(prog)s [options] file")
parser_translate.add_argument("file",
                              action="store",
                              nargs=1)
parser_translate.add_argument("--out",
                              action="store",
                              nargs=1,
                              help="place the output into <file>.",
                              metavar="<file>")
parser_translate.set_defaults(func=translate)

parser_run = subparsers.add_parser("run",
                                   usage="%(prog)s [options] file")
parser_run.add_argument("file",
                        action="store",
                        nargs=1)
parser_run.add_argument("--cc",
                        action="store",
                        nargs=1,
                        default=["cc"],
                        help="c compiler to be used (default: `cc`)",
                        metavar="<cc>")
parser_run.set_defaults(func=run)

def main():
    args = parser.parse_args()
    if args.version:
        sys.exit(__version__)
    if args.func:
        try:
            args.func(args)
        except Exception as e:
            sys.exit(e)
    else:
        parse.print_help()
