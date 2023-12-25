from sys import argv, stderr

from lexer import my_lexer, tokens  # noqa: F401
from ply import yacc

precedence = (
    ("left", "AND_KW", "OR_KW"),
    ("left", "ADD_OP", "SUB_OP"),
    ("left", "MUL_OP", "DIV_OP"),
)


def p_start(p):
    """
    start : PROGRAM_KW IDENTIFIER SEMICOLON decList funcList block
    """
    _ = p


def p_decList(p):
    """
    decList : decs decListRest
    """
    _ = p


def p_decListRest(p):
    """
    decListRest : decs decListRest
            |
    """
    _ = p


def p_decs(p):
    """
    decs : type varList SEMICOLON
         |
    """
    _ = p


def p_type(p):
    """
    type : INTEGER_KW
         | REAL_KW
         | BOOLEAN_KW
    """
    _ = p


def p_varList(p):
    """
    varList : IDENTIFIER varListRest
    """
    _ = p


def p_varListRest(p):
    """
    varListRest : COMMA IDENTIFIER varListRest
                |
    """
    _ = p


def p_funcList(p):
    """
    funcList : FUNCTION_KW IDENTIFIER parameters COLON type decList block SEMICOLON
             |
    """
    _ = p


def p_parameters(p):
    """
    parameters : LEFT_PA decList RIGHT_PA
    """
    _ = p


def p_block(p):
    """
    block : BEGIN_KW stmtList END_KW SEMICOLON
    """
    _ = p


def p_stmtList(p):
    """
    stmtList : stmt
             | stmtList stmt
    """
    _ = p


def p_stmt(p):
    """
    stmt : IDENTIFIER ASSIGN_OP expr SEMICOLON
         | IF_KW expr THEN_KW stmt matchedStmt
         | WHILE_KW expr DO_KW stmt
         | FOR_KW IDENTIFIER ASSIGN_OP expr TO_KW expr DO_KW stmt
         | RETURN_KW expr SEMICOLON
         | expr
         | block
    """
    _ = p


def p_matchedStmt(p):
    """
    matchedStmt : ELSE_KW stmt
                |
    """
    _ = p


def p_expr(p):
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
    _ = p


def p_relop(p):
    """
    relop : LT_OP
          | LE_OP
          | NE_OP
          | EQ_OP
          | GE_OP
          | GT_OP
    """
    _ = p


def p_error(p):
    print("Whoa. You are seriously hosed.", file=stderr)
    if not p:
        print("End of File!", file=stderr)
        return

    # Read ahead looking for a closing 'block'
    while True:
        tok = parser.token()  # Get the next token
        print(tok)
        if not tok or tok.type == "END_KW":
            break
    parser.restart()


# method: 'SLR', 'LALR'
parser = yacc.yacc(method="SLR")

if __name__ == "__main__":
    input_txt = open(argv[1]).read()
    parser.parse(
        input=input_txt,
        debug=True,
        lexer=my_lexer,
    )
