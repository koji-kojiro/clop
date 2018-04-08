import sys
from .read import read
from .syntax import functions, special_forms

def parse_declaration(declartion):
    if ":" in declartion:
        specifier, identifier = declartion.split(":")
        return specifier.replace("-", " ") + " " +  identifier
    else:
        return declartion

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
        return parse_declaration(sexp)

def translate_file(fname, dest=sys.stdout):
    with open(fname, "r") as fp:
        form = read(fp)
        toplevel_forms = []
        while(form):
            toplevel_forms.append(sexp2c(form))
            form = read(fp)
        code = ""
        for form in toplevel_forms:
            if form:
                if form[-1] in " {};" or form[0] in "#/":
                    form += "\n"
                elif form is not "\n":
                    form += ";\n"
            code += form
        dest.write(code)
