from ply import lex

keywords = {
    "program": "PROGRAM_KW",
    "function": "FUNCTION_KW",
    "begin": "BEGIN_KW",
    "end": "END_KW",
    "while": "WHILE_KW",
    "do": "DO_KW",
    "for": "FOR_KW",
    "to": "TO_KW",
    "if": "IF_KW",
    "then": "THEN_KW",
    "else": "ELSE_KW",
    "integer": "INTEGER_KW",
    "real": "REAL_KW",
    "boolean": "BOOLEAN_KW",
    "return": "RETURN_KW",
    "and": "AND_KW",
    "or": "OR_KW",
    "true": "TRUE_KW",
    "false": "FALSE_KW",
}

tokens = tuple(keywords.values()) + (
    "IDENTIFIER",
    "NUMBER",
    "ASSIGN_OP",
    "MUL_OP",
    "DIV_OP",
    "ADD_OP",
    "SUB_OP",
    "LT_OP",
    "LE_OP",
    "NE_OP",
    "EQ_OP",
    "GE_OP",
    "GT_OP",
    "COLON",
    "SEMICOLON",
    "COMMA",
    "RIGHT_PA",
    "LEFT_PA",
)

# rules
t_ignore = "\t "
t_PROGRAM_KW = r"program"
t_FUNCTION_KW = r"function"
t_BEGIN_KW = r"begin"
t_END_KW = r"end"
t_WHILE_KW = r"while"
t_DO_KW = r"do"
t_FOR_KW = r"for"
t_TO_KW = r"to"
t_IF_KW = r"if"
t_THEN_KW = r"then"
t_ELSE_KW = r"else"
t_INTEGER_KW = r"integer"
t_REAL_KW = r"real"
t_BOOLEAN_KW = r"boolean"
t_RETURN_KW = r"return"
t_AND_KW = r"and"
t_OR_KW = r"or"
t_TRUE_KW = r"true"
t_FALSE_KW = r"false"
t_NUMBER = r"(\d+)(\.\d+)?"
t_ASSIGN_OP = r":="
t_MUL_OP = r"\*"
t_DIV_OP = r"/"
t_ADD_OP = r"\+"
t_SUB_OP = r"-"
t_LT_OP = r"<"
t_LE_OP = r"<="
t_NE_OP = r"<>"
t_EQ_OP = r"="
t_GE_OP = r">="
t_GT_OP = r">"
t_COLON = r":"
t_SEMICOLON = r";"
t_COMMA = r","
t_LEFT_PA = r"\("
t_RIGHT_PA = r"\)"

table: dict[str, int] = {}  # gotta change it for symbol table.
last = 1


def t_newline(t):
    r"\n+"
    t.lexer.lineno += len(t.value)


def t_IDENTIFIER(tok):
    r"[a-zA-Z_][a-zA-Z_0-9]*"
    tok.type = keywords.get(tok.value, "IDENTIFIER")
    return tok


def t_error(tok):
    tok.lexer.skip(1)


my_lexer = lex.lex()

if __name__ == "__main__":
    from sys import argv, stderr, stdout

    argc = len(argv)
    table = {}

    if argc < 2:
        print("ERROR: need a input file", file=stderr)
        exit(-1)

    if argc > 3:
        print("ERROR: too much file to handle.", file=stderr)
        exit(-1)

    if argc == 2:
        out = stdout
    else:
        try:
            out = open(argv[2], "w")
        except OSError:
            exit(1)

    try:
        input_file = open(argv[1], "r")
    except OSError:
        print("ERROR: can't open input file!", file=stderr)
        exit(-1)

    input_txt = input_file.read()
    my_lexer.input(input_txt)
    last = 1

    for tok in my_lexer:
        if tok.type in ["IDENTIFIER", "NUMBER"]:
            if tok.value not in table:
                table[tok.value] = last
                last += 1
        print(f"{tok.value}\t<{tok.type},{table.get(tok.value,'-')}>", file=out)
