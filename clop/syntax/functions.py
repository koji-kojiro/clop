from .utils import block

def aref(array, subscript):
    return f"{array}[{subscript}]"

def break_():
    return "break"

def comment(line):
    return f"//{line}"

def continue_():
    return "continue"

def declare(*declarations):
    return "\n".join(declarations)

def defvar(name, value=None):
    return f"{name} = {value}" if value else name

def include(header):
    return f"#include <{header}.h>"

def return_(value):
    return f"return {value}" 

def when(test, *body):
    return f"if ({test}) " + block(body)

functions = {
    "aref": aref,
    "break": break_,
    "continue": continue_,
    "comment": comment,
    "declare": declare,
    "defvar": defvar,
    "include": include,
    "return": return_,
    "when": when,
}

