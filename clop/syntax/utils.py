def block(statements):
    statements = list(statements)
    code = "\n"
    for statement in statements:
        for line in filter(len, statement.split("\n")):
            code += "  " + line
            if code[-1] in " {};" or line.startswith("/"):
                code += "\n"
            else:
                code += ";\n"
    return "{" + code + "}" if len(statements) > 1 else code


