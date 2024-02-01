from lexer import LEXER
from ply.yacc import YaccProduction, yacc
from ply.lex import LexToken

precedence = (
    ("left", "AND_KW", "OR_KW"),
    ("left", "ADD_OP", "SUB_OP"),
    ("left", "MUL_OP", "DIV_OP"),
)

code: str = ""


class MySyntaxError(Exception):

    def __init__(self, p: YaccProduction | LexToken, *args: object) -> None:
        self.p = p
        super().__init__(*args)


def p_start(p: YaccProduction):
    """
    start : PROGRAM_KW IDENTIFIER SEMICOLON decList funcList block
    """
    global code
    p[0] = f"""#include <stdbool.h>
{p[4]}
{p[5]}
int main(int argc, char** argv){p[6]}
"""
    code = str(p[0])


def p_decList(p: YaccProduction):
    """
    decList : decs decListRest
    """
    p[0] = f"// variable decralation:\n{p[1]}"


def p_decListRest(p: YaccProduction):
    """
    decListRest : decs decListRest
                |
    """
    if len(p) == 1:
        p[0] = ""
    else:
        p[0] = p[1]


def p_decs(p: YaccProduction):
    """
    decs : type varList SEMICOLON
         |
    """
    if len(p) == 1:
        p[0] = ""
        return

    if p[1] == "real":
        p[0] = f"float {p[2]};\n"
    elif p[1] == "integer":
        p[0] = f"int {p[2]}\n"
    elif p[1] == "bool ean":
        p[0] = f"bool {p[2]}\n"
    else:
        raise ValueError("WHUT??")


def p_type(p: YaccProduction):
    """
    type : INTEGER_KW
         | REAL_KW
         | BOOLEAN_KW
    """
    p[0] = p[1]


def p_varList(p: YaccProduction):
    """
    varList : IDENTIFIER varListRest
    """
    p[0] = f"{p[1]}{p[2]};"


def p_varListRest(p: YaccProduction):
    """
    varListRest : COMMA IDENTIFIER varListRest
                |
    """
    if len(p) == 1:
        p[0] = ""
        return
    p[0] = f", {p[2]}{p[3]}"


def p_funcList(p: YaccProduction):
    """
    funcList : FUNCTION_KW IDENTIFIER parameters COLON type decList block
             |
    """
    if len(p) == 1:
        p[0] = "// no function created\n"
        return
    p[0] = "// functions:\n"
    if p[5] == "real":
        p[5] = "float"
    elif p[5] == "integer":
        p[5] = "int"
    elif p[5] == "boolean":
        p[5] = "bool"
    else:
        raise ValueError("WHUT? 2")

    p[0] += f"{p[5]} {p[2]}{p[3]} {p[7]}"


def p_parameters(p: YaccProduction):
    """
    parameters : LEFT_PA decList RIGHT_PA
    """
    p[0] = f"({p[2]})"


def p_block(p: YaccProduction):
    """
    block : BEGIN_KW stmtList END_KW
    """
    p[0] = f"{{\n// block start\n{p[2]}// block end\n}}"


def p_stmtList(p: YaccProduction):
    """
    stmtList : stmt
             | stmtList stmt
    """
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[1] + p[2]


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
    p[0] = p[1:]
    if len(p) < 3:
        p[0] = p[1]
        return

    if p[1] == "if":
        p[0] = f"if ({p[2]}) {p[4]}\n"
    elif p[1] == "while":
        p[0] = f"while ({p[2]}) {p[4]}\n"
    elif p[1] == "for":
        p[0] = f"for ({p[2]}={p[4]}; {p[2]}<{p[6]}; {p[2]}++) {p[8]}\n"
    elif p[1] == "return":
        p[0] = f"return {p[2]};\n"
    elif p[2] == ":=":
        p[0] = f"{p[1]} = {p[3]};\n"


def p_matchedStmt(p: YaccProduction):
    """
    matchedStmt : ELSE_KW stmt
                |
    """
    if len(p) > 1:
        p[0] = f"else {p[1]}\n"
        return
    p[0] = ""


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
         | IDENTIFIER LEFT_PA actualParamList RIGHT_PA
         | IDENTIFIER
         | NUMBER
         | TRUE_KW
         | FALSE_KW
    """
    if len(p) == 5:
        p[0] = f"{p[1]}({p[3]})"
    elif len(p) == 4:
        p[0] = f"{p[1]} {p[2]} {p[3]}"
    elif len(p) == 2:
        p[0] = f"{p[1]}"
    else:
        raise ValueError("WHUT? 3")


def p_actualParamList(p: YaccProduction):
    """
    actualParamList : expr
                    | actualParamList COMMA expr
                    | IDENTIFIER
                    | NUMBER
                    |
    """
    if len(p) == 1:
        p[0] = ""
    elif len(p) == 2:
        p[0] = p[1]
    elif len(p) == 3:
        p[0] = f"{p[1]}, {p[2]}"


def p_relop(p: YaccProduction):
    """
    relop : LT_OP
          | LE_OP
          | NE_OP
          | EQ_OP
          | GE_OP
          | GT_OP
    """
    if p[1] == "=":
        p[0] = "=="
        return
    p[0] = p[1]


def p_error(p: LexToken):
    raise MySyntaxError(p, f"error at line {p.lineno}")


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
        p = e.p
        print(p.lineno, file=stderr)
    finally:
        # print(*__productions, sep="\n", file=out_file)
        pass

    print(code, file=out_file)

    out_file.close()
