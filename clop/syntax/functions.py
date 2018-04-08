from .utils import block

def break_():
    return "break"

def continue_():
    return "continue"

def include(header):
    return f"#include <{header}.h>"

def return_(value):
    return f"return {value}" 

def when(test, *body):
    return f"if ({test}) " + block(body)

def comment(line):
    return f"//{line}"

functions = {
    "break": break_,
    "continue": continue_,
    "comment": comment,
    "include": include,
    "return": return_,
    "when": when,
}

