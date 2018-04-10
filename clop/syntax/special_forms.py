from string import ascii_letters, digits
from .utils import block, implicit_forms

def cond(hook, clause, *clauses):
    clause = list(map(hook, clause))
    code = f"if ({clause[0]}) " + block(clause[1:])
    for caluse in clauses:
        clause = list(map(hook, caluse))
        code += f"else if ({clause[0]}) " + block(clause[1:])
    return code

def defun(hook, declaration, args_list, *body):
    declaration = hook(declaration)
    args_list = list(map(hook, args_list))
    code = "{} ({})\n".format(declaration, ", ".join(args_list))
    if len(declaration) > 3 and declaration[-4:] != "main":
        ptypes = []
        for arg in args_list:
            ptype = " ".join(arg.split()[:-1])
            for c in arg.split()[-1]:
                if c not in ascii_letters + digits + "_":
                    ptype += c
            ptypes.append(ptype)
        implicit_forms.insert(0, "\n{} ({})".format(declaration, ", ".join(ptypes)))
    if len(body) == 1:
        body = ("\n",) + body
    return code + block(map(hook, body))

def defstruct(hook, name, members):
    code = f"\ntypedef struct {name} "
    implicit_forms.insert(0, code + block(map(hook, members)) + f" {name}")
    return ""

def parse_macro_args(argslist):
    args_map = dict()
    for n, arg in enumerate(argslist):
        if isinstance(arg, list):
            for m, a in enumerate(arg):
                args_map.update({a: f"args[{n}][{m}]"})
        elif arg == "&body":
            args_map.update({argslist[int(n) + 1]: f"args[{n}:]"})
            break
        else:
            args_map.update({arg: f"args[{n}]"})
    return args_map

def expand_macro_body(body, args, args_map):
    expanded = []
    for elm in body:
        if isinstance(elm, str):
            for k, v in args_map.items():
                value = eval(v)
                if isinstance(value, str):
                    elm = elm.replace("," + k, value)
                else:
                    if elm == "," + k:
                        elm = list(value)
                    elif elm == ",@" + k:
                        elm = value
            if isinstance(elm, str) or isinstance(elm, list):
                expanded.append(elm)
            else:
                expanded.extend(elm)
        else:
            expanded.append(expand_macro_body(elm, args, args_map))
    return expanded

def defsyntax(hook, name, argslist, body):
    args_map = parse_macro_args(argslist)
    def macro_function(hook, *args):
        expanded = hook(expand_macro_body(body, args, args_map))
        return expanded
    special_forms.update({name: macro_function})
    return "\n"

def defunion(hook, name, members):
    code = f"\ntypedef union {name} "
    implicit_forms.insert(0, code + block(map(hook, members)) + f" {name}")
    return ""

def defenum(hook, name, members):
    code = f"\ntypedef enum {name}"
    implicit_forms.insert(0, code + "{{\n{}\n}} {}".format(",\n".join(map("  ".__add__, members)), name))
    return ""

def for_(hook, forms, *body):
    for n in range(3 - len(forms)):
        forms += ("", )
    code =  "for ({}) ".format(("; " if forms[1] else ";").join(map(hook, forms)))
    return code + block(map(hook, body))

def let(hook, definitions, *body):
    for definition in definitions[::-1]:
        definition = list(map(hook, definition))
        if len(definition) > 1:
            body = (f"{definition[0]} = {definition[1]}",) + body
        else:
            body = (f"{definition[0]}", ) + body
    return "({})".format(block(map(hook, body)))

def while_(hook, test, *body):
    code = "while ({}) ".format(hook(test))
    return code + block(map(hook, body))
    
special_forms = {
    "cond": cond,
    "defun": defun,
    "defstruct": defstruct,
    "defsyntax": defsyntax,
    "defunion": defunion,
    "defenum": defenum,
    "for": for_,
    "let": let,
    "while": while_,
}
