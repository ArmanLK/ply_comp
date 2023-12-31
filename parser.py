from lexer import my_lexer, tokens
from ply import yacc
from ply.lex import LexToken

precedence = (
    ("left", "AND_KW", "OR_KW"),
    ("left", "ADD_OP", "SUB_OP"),
    ("left", "MUL_OP", "DIV_OP"),
)


__productions = []


def __production_to_string(slice: list) -> str:
    if slice == []:
        return ""

    return f'{slice[0]} -> {"".join(__token_to_string(tok) for tok in slice[1:])}'


def __token_to_string(token: LexToken) -> str:  # this is ugly!
    if token.type not in tokens:
        return f"{token.type} "
    return f'"{token.value}" '


def p_start(p):
    """
    start : PROGRAM_KW IDENTIFIER SEMICOLON decList funcList block
    """
    __productions.append(__production_to_string(p.slice))


def p_decList(p):
    """
    decList : decs decListRest
    """
    __productions.append(__production_to_string(p.slice))


def p_decListRest(p):
    """
    decListRest : decs decListRest
            |
    """
    __productions.append(__production_to_string(p.slice))


def p_decs(p):
    """
    decs : type varList SEMICOLON
         |
    """
    __productions.append(__production_to_string(p.slice))


def p_type(p):
    """
    type : INTEGER_KW
         | REAL_KW
         | BOOLEAN_KW
    """
    __productions.append(__production_to_string(p.slice))


def p_varList(p):
    """
    varList : IDENTIFIER varListRest
    """
    __productions.append(__production_to_string(p.slice))


def p_varListRest(p):
    """
    varListRest : COMMA IDENTIFIER varListRest
                |
    """
    __productions.append(__production_to_string(p.slice))


def p_funcList(p):
    """
    funcList : FUNCTION_KW IDENTIFIER parameters COLON type decList block SEMICOLON
             |
    """
    __productions.append(__production_to_string(p.slice))


def p_parameters(p):
    """
    parameters : LEFT_PA decList RIGHT_PA
    """
    __productions.append(__production_to_string(p.slice))


def p_block(p):
    """
    block : BEGIN_KW stmtList END_KW SEMICOLON
    """
    __productions.append(__production_to_string(p.slice))


def p_stmtList(p):
    """
    stmtList : stmt
             | stmtList stmt
    """
    __productions.append(__production_to_string(p.slice))


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
    __productions.append(__production_to_string(p.slice))


def p_matchedStmt(p):
    """
    matchedStmt : ELSE_KW stmt
                |
    """
    __productions.append(__production_to_string(p.slice))


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
    __productions.append(__production_to_string(p.slice))


def p_relop(p):
    """
    relop : LT_OP
          | LE_OP
          | NE_OP
          | EQ_OP
          | GE_OP
          | GT_OP
    """
    __productions.append(__production_to_string(p.slice))


def p_error(p):  # I don't care about errors
    _ = p
    pass


# method: 'SLR', 'LALR'
parser = yacc.yacc(method="SLR")

if __name__ == "__main__":
    from sys import argv, stderr

    try:
        input_txt = open(argv[1]).read()
    except Exception as e:
        print(e, stderr)
        exit()

    parser.parse(
        input=input_txt,
        lexer=my_lexer,
    )
    print(*__productions, sep="\n")
