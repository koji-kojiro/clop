c_binops = {"+", "-", ">>", "<<", "=",}

def binary_operator(char):
    def operator_func(*terms):
        terms = list(terms)
        for n, term in enumerate(terms):
            if term.startswith("("):
                continue
            for op in c_binops:
                op = f" {op} "
                if op in term:
                    terms[n] = f"({term})"
        return f" {char} ".join(terms)
    return operator_func

def unary_operator(char):
    def operator_func(term):
        for op in c_binops:
            if op in term:
                term = f"({term})"
        return f"{char}{term}"
    return operator_func

operators = {
    "+": binary_operator("+"),
    "-": binary_operator("-"),
    "*": binary_operator("*"),
    "/": binary_operator("/"),
    "mod": binary_operator("%"),
    "eq": binary_operator("=="),
    "<": binary_operator("<"),
    ">": binary_operator(">"),
    "logand": binary_operator("&"),
    "logior": binary_operator("|"),
    "logxor": binary_operator("^"),
    "ash": binary_operator(">>"),
    "and": binary_operator("&&"),
    "or": binary_operator("||"),
    "not": unary_operator("!"),
}
