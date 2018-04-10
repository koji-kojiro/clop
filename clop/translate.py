import os
import re
import sys
import string
from .read import read
from .syntax import functions, special_forms, implicit_forms, load_path

buitin_names = [j for i in (functions, special_forms) for j in i.keys()]

def convert_name(name):
    if len(name) > 3:
        if name.startswith("+") and name.endswith("+"):
            name = name[1:-1].upper()
        if len(name) > 3 and name not in buitin_names:
            name = re.sub("-(?!\>)", "_", name)
    return name

def parse_name(name):
    if ":" in name:
        name = name.split(":")
        identifier = convert_name(name[-1])
        specifier = " ".join(name[:-1])
        return specifier + " " +  identifier
    else:
        return convert_name(name)

def call(function, *args):
    return "{}({})".format(function, ", ".join(args))

def sexp2c(sexp):
    if type(sexp) is list:
        function = sexp[0]
        if function in functions.keys():
            return functions[function](*list(map(sexp2c, sexp[1:])))
        elif function in special_forms.keys():
            return special_forms[function](sexp2c, *sexp[1:])
        else:
            return call(*list(map(sexp2c, sexp)))
    else:
        return parse_name(sexp)

def translate_file(fname, dest=sys.stdout):
    load_path.append(os.path.abspath(os.path.dirname(fname)))
    with open(fname, "r") as fp:
        form = read(fp)
        toplevel_forms = []
        while(form):
            toplevel_forms.append(sexp2c(form))
            form = read(fp)
        for n, form in enumerate(toplevel_forms):
            if form[0] != "#":
                for iform in implicit_forms:
                    toplevel_forms.insert(n, iform)
                break
        else:
            if implicit_forms:
                implicit_forms.insert(0, "\n")
            toplevel_forms.extend(implicit_forms)
        code = ""
        extra_lines = 0
        for form in toplevel_forms:
            if all(map(lambda _: _ in string.whitespace, form)):
                extra_lines += 1
            else:
                extra_lines = 0
            if form:
                if form[-1] in " {};" or form[0] in "#/":
                    form += "\n"
                elif form is not "\n":
                    form += ";\n"
            if extra_lines < 2:        
                code += form
        dest.write(code)
