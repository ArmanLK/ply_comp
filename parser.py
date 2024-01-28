from lexer import LEXER, tokens
from ply.yacc import YaccProduction, yacc
from ply.lex import LexToken

precedence = (
    ("left", "AND_KW", "OR_KW"),
    ("left", "ADD_OP", "SUB_OP"),
    ("left", "MUL_OP", "DIV_OP"),
)


__productions = []


def __production_to_string(p: YaccProduction) -> str:
    if p.slice == []:
        return ""

    s = str().join(__token_to_string(tok) for tok in p.slice[1:])
    return f"{p.number}\t\t{p.slice[0]} -> {s}"


def __token_to_string(token: LexToken) -> str:
    if token.type not in tokens:
        return f"{token.type} "
    return f'"{token.value}" '


class MySyntaxError(Exception):
    def __init__(self, lineno, *args: object) -> None:
        self.lineno = lineno
        super().__init__(*args)


def p_start(p: YaccProduction):
    """
    start : PROGRAM_KW IDENTIFIER SEMICOLON decList funcList block
    """
    __productions.append(__production_to_string(p))


def p_decList(p: YaccProduction):
    """
    decList : decs decListRest
    """
    __productions.append(__production_to_string(p))


def p_decListRest(p: YaccProduction):
    """
    decListRest : decs decListRest
                |
    """
    __productions.append(__production_to_string(p))


def p_decs(p: YaccProduction):
    """
    decs : type varList SEMICOLON
         |
    """
    __productions.append(__production_to_string(p))


def p_type(p: YaccProduction):
    """
    type : INTEGER_KW
         | REAL_KW
         | BOOLEAN_KW
    """
    __productions.append(__production_to_string(p))


def p_varList(p: YaccProduction):
    """
    varList : IDENTIFIER varListRest
    """
    __productions.append(__production_to_string(p))


def p_varListRest(p: YaccProduction):
    """
    varListRest : COMMA IDENTIFIER varListRest
                |
    """
    __productions.append(__production_to_string(p))


def p_funcList(p: YaccProduction):
    """
    funcList : FUNCTION_KW IDENTIFIER parameters COLON type decList block
             |
    """
    __productions.append(__production_to_string(p))


def p_parameters(p: YaccProduction):
    """
    parameters : LEFT_PA decList RIGHT_PA
    """
    __productions.append(__production_to_string(p))


def p_block(p: YaccProduction):
    """
    block : BEGIN_KW stmtList END_KW
    """
    __productions.append(__production_to_string(p))


def p_stmtList(p: YaccProduction):
    """
    stmtList : stmt
             | stmtList stmt
    """
    __productions.append(__production_to_string(p))
    # print(p[:])


def p_stmt(p: YaccProduction):
    """
    stmt : IDENTIFIER ASSIGN_OP expr SEMICOLON
         | IF_KW expr THEN_KW stmt matchedStmt
         | WHILE_KW expr DO_KW stmt
         | FOR_KW IDENTIFIER ASSIGN_OP expr TO_KW expr DO_KW stmt
         | RETURN_KW expr SEMICOLON
         | expr
         | block
    """
    __productions.append(__production_to_string(p))
    # print(p[:])


def p_matchedStmt(p: YaccProduction):
    """
    matchedStmt : ELSE_KW stmt
                |
    """
    __productions.append(__production_to_string(p))
    # print(p[:])


def p_expr(p: YaccProduction):
    """
    expr : expr AND_KW expr
         | expr OR_KW expr
         | expr MUL_OP expr
         | expr DIV_OP expr
         | expr ADD_OP expr
         | expr SUB_OP expr
         | expr relop expr
         | LEFT_PA expr RIGHT_PA
         | IDENTIFIER
         | NUMBER
         | TRUE_KW
         | FALSE_KW
    """
    __productions.append(__production_to_string(p))
    if len(p) == 4:
        p[0] = p[1] + p[2] + p[3]
        return
    p[0] = p[1]


def p_relop(p: YaccProduction):
    """
    relop : LT_OP
          | LE_OP
          | NE_OP
          | EQ_OP
          | GE_OP
          | GT_OP
    """
    __productions.append(__production_to_string(p))
    p[0] = p[1]


def p_error(p: LexToken | YaccProduction):
    raise MySyntaxError(p.lineno, f"error at line {p.lineno}")


# method: 'SLR', 'LALR'
PARSER = yacc(method="SLR")

if __name__ == "__main__":
    from sys import argv, stderr, stdout

    try:
        out_file = open(argv[2])
    except IndexError:
        out_file = stdout

    try:
        input_file = open(argv[1])
        input_txt = input_file.read()
        input_file.close()
    except Exception as e:
        print(e, stderr)
        exit()

    try:
        PARSER.parse(
            input=input_txt,
            # debug=True,
            lexer=LEXER,
        )
    except MySyntaxError as e:
        print(e.lineno, file=stderr)
    finally:
        print(*__productions, sep="\n", file=out_file)
        pass

    out_file.close()
