from .utils import block

def defun(hook, declartion, args_list, *body):
    code = "{} ({})\n".format(hook(declartion), ", ".join(map(hook, args_list)))
    return code + block(map(hook, body))

def defstruct(hook, name, members):
    code = f"typedef struct {name} "
    return code + block(map(hook, members)) + f" {name}"

def defunion(hook, name, members):
    code = f"typedef union {name} "
    return code + block(map(hook, members)) + f" {name}"

def defenum(hook, name, members):
    code = f"typedef enum {name}"
    return code + "{{\n{}\n}} {}".format(",\n".join(map("  ".__add__, members)), name)
    

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
    return block(map(hook, body))

def while_(hook, test, *body):
    code = "while ({}) ".format(hook(test))
    return code + block(map(hook, body))
    

special_forms = {
    "defun": defun,
    "defstruct": defstruct,
    "defunion": defunion,
    "defenum": defenum,
    "for": for_,
    "let": let,
    "while": while_,
}
