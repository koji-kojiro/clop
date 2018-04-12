from .utils import block, implicit_forms

def aref(array, subscript):
    return f"{array}[{subscript}]"

def break_():
    return "break"

def cast(obj, rettype):
    return f"({rettype})obj"

def continue_():
    return "continue"

def decf(place, value=1):
    if value == 1:
        return f"++{place}"
    return f"{place} -= {value}"

def declare(*declarations):
    return "\n".join(declarations)

def defconstant(name, value):
    return f"#define {name} {value}"

def defvar(name, value=None):
    return f"{name} = {value}" if value else name

def if_(test, trueform, falseform):
    return f"{test}? ({trueform}) : ({falseform})"

def incf(place, value=1):
    if value == 1:
        return f"++{place}"
    return f"{place} += {value}"

known_headers = []
def include(header):
    if not header in known_headers:
        implicit_forms.insert(0, f"#include <{header}.h>")
        known_headers.append(header)
    return "\n"

def progn(*forms):
    return "({})".format(block(forms))

def return_(value):
    return f"return {value}" 

def setf(*pairs):
    code = []
    for place, value in zip(pairs[::2], pairs[1::2]):
        code.append(f"{place} = {value}")
    return "\n".join(code)

def when(test, *body):
    return "({{{}}})".format(f"if ({test}) " + block(body))

def one_plus(variable):
    return f"{variable} + 1"

def one_minus(variable):
    return f"{variable} - 1"

functions = {
    "aref": aref,
    "break": break_,
    "cast": cast,
    "continue": continue_,
    "decf": decf,
    "declare": declare,
    "defvar": defvar,
    "defconstant": defconstant,
    "if": if_,
    "incf": incf,
    "include": include,
    "progn": progn,
    "return": return_,
    "setf": setf,
    "when": when,
    "1+": one_plus,
    "1-": one_minus,
}

