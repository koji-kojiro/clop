import os
from string import ascii_letters, digits
from clop.read import read
from .misc import block, implicit_forms, load_path

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

def parse_macro_args(args, argslist):
    argslist = argslist[:]
    key_pos = [n for n, a in enumerate(args) if str(a).startswith(":")]
    given_keys = {args[n][1:]: args[n + 1] for n in key_pos}
    args = [a for n, a in enumerate(args) if not n in key_pos]
 
    args_map = {}
    optional = False
    keyword = False
    
    while(argslist):
        spec = argslist.pop(0)
        if isinstance(spec, list):
            if optional:
                name = spec[0]
                value = args.pop(0) if args else spec[1]
            elif keyword:
                name = spec[0]
                if name in given_keys:
                    value = given_keys.pop(name)
                else:
                    value = spec[1]
            else:
                sub_map = parse_macro_args(args.pop(0), spec)
                args_map.update(sub_map)
                continue
        elif spec == "&optional":
            optional, keyword = True, False
            continue
        elif spec == "&key":
            optional, keyword = False, True
            continue
        elif spec in {"&rest", "&body"}:
            args_map.update({argslist.pop(0): tuple(args)})
            break
        else:
            name = spec
            if optional:
                value = args.pop(0) if args else 0
            elif keyword:
                continue
            else:
                value = args.pop(0)
        args_map.update({name: value})
    return args_map

def expand_macro_body(body, args_map):
    expanded = []
    for elm in body:
        if isinstance(elm, str):
            if not elm[0] in "\"'":
                for name, value in args_map.items():
                    if isinstance(value, str):
                        elm = elm.replace("," + name, value)
                    else:
                        if elm == "," + name:
                            elm = list(value)
                            break
                        elif elm == ",@" + name:
                            elm = value
                            break
            if isinstance(elm, str) or isinstance(elm, list):
                expanded.append(elm)
            else:
                expanded.extend(elm)
        else:
            expanded.append(expand_macro_body(elm, args_map))
    return expanded

def defsyntax(hook, name, argslist, body):
    def macro_function(hook, *args):
        try:
            args_map = parse_macro_args(args, argslist)
        except IndexError:
            import traceback
            traceback.print_exc()
            raise ValueError(f"{name} expected even more arguments")
        expanded = hook(expand_macro_body(body, args_map))
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

def extract_macro_definitions(sexp):
    definitions = []
    for elm in sexp:
        if isinstance(elm, str):
            if elm in ("defsyntax", "include"):
                definitions.append(sexp)
                break
        else:
            definitions.extend(extract_macro_definitions(elm))
    return list(filter(len, definitions))

known_modules = []
def require(hook, module):
    if module in known_modules:
        return "\n"
    known_modules.append(module)
    module_dir = ""
    if "." in module:
        module_dir = "/".join(module.split(".")[:-1])
        module = module.split(".")[-1]
    for path in load_path:
        try:
            path = os.path.join(path, module_dir)
            if module + ".clop" in os.listdir(path):
                fname = os.path.join(path, module + ".clop")
                break
        except OSError:
            pass
    else:
        raise ImportError(f"No such file:{module}.clop")
    forms = []
    with open(fname, "r") as fp:
        form = read(fp)
        while(form):
            forms.append(form)
            form = read(fp)
    forms = extract_macro_definitions(forms)
    for form in forms:
        hook(form)
    return "\n"

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
    "require": require,
    "while": while_,
}
