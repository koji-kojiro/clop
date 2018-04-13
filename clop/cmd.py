import os
import sys
import argparse
import tempfile
import subprocess
from clop import __version__
from clop.translate import translate_file

def translate(args):
    if args.out:
        with open(args.out[0], "w") as fp:
            translate_file(args.file, fp)
    else:
        translate_file(args.file)

def run(args):
    cwd = os.path.abspath("./")
    with tempfile.TemporaryDirectory(prefix="clop-run", dir=cwd) as dstdir:
        target = os.path.join(dstdir, "a.c")
        with open(target, "w") as fp:
            translate_file(args.file, fp)
        os.chdir(dstdir)
        cmd = [args.cc, "a.c", "-o", "clop-run.out"]
        cmd.extend(args.flags)
        subprocess.check_output(cmd)
        os.chdir("../")
        cmd = [os.path.join(dstdir, "clop-run.out")]
        if args.args:
            cmd.extend(args.args[0].split(" "))
        ret = subprocess.call(cmd)
    if ret is not 0:
        print(f"\x1b[31mwarning: {args.file} returned non-zero status {ret}\x1b[0m")
    sys.exit(ret)

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
                              nargs=1,
                              help="source file to be translated")
parser_translate.add_argument("--out",
                              action="store",
                              nargs=1,
                              help="place the output into <file>.",
                              metavar="<file>")
parser_translate.set_defaults(func=translate)

parser_run = subparsers.add_parser("run",
                                   usage="%(prog)s [options] file [[--] flags...]")
parser_run.add_argument("file",
                        action="store",
                        help="source file to be run as a script")
parser_run.add_argument("flags",
                        nargs=argparse.REMAINDER,
                        help="options to be passed to the c compiler")
parser_run.add_argument("--cc",
                        action="store",
                        default="cc",
                        help="c compiler to be used (default: `cc`)",
                        metavar="<cc>")
parser_run.add_argument("--args",
                        action="store",
                        nargs=1,
                        help="arguments to be passed to the program",
                        metavar="<args>")
parser_run.set_defaults(func=run)

def main():
    args = parser.parse_args()
    if args.version:
        sys.exit(__version__)
    if hasattr(args, "func"):
        try:
            args.func(args)
        except Exception as e:
            sys.exit("\x1b[31m{}: {}\x1b[0m".format(type(e).__name__, e))
    else:
        parser.print_help()
