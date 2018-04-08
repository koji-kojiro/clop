from .utils import block

def aref(array, subscript):
    return f"{array}[{subscript}]"

def break_():
    return "break"

def cast(obj, rettype):
    return f"({rettype})obj"

def comment(line):
    return f"//{line}"

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

def if_(test, trueform, falseform=None):
    code = f"if ({test}) \n  {trueform}"
    if falseform:
        code += f"\nelse \n  {falseform}"
    return code

def incf(place, value=1):
    if value == 1:
        return f"++{place}"
    return f"{place} += {value}"

def include(header):
    return f"#include <{header}.h>"

def progn(*forms):
    return block(forms)

def return_(value):
    return f"return {value}" 

def setf(*pairs):
    code = []
    for place, value in zip(pairs[::2], pairs[1::2]):
        code.append(f"{place} = {value}")
    return "\n".join(code)

def when(test, *body):
    return f"if ({test}) " + block(body)

def one_plus(variable):
    return f"{variable + 1}"

def one_minus(variable):
    return f"{variable - 1}"

functions = {
    "aref": aref,
    "break": break_,
    "cast": cast,
    "continue": continue_,
    "comment": comment,
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

