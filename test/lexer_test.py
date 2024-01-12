from unittest import TestCase
import unittest

from lexer import LEXER


class LexerTest(TestCase):
    def test1(self):
        """It's hell of a unit test."""
        test_input: str = """
        program prg1;
        integer num,divisor,quotient;
        begin
        num:=61;
        divisor:=2;
        quotient:=0;
        if num=1 then
        return false;
        else if num = 2 then
        return true;
        while divisor<=(num/2) do
        begin
        quotient:=num/divisor;
        if divisor * quotient=num then
        return false;
        divisor:=divisor+1;
        end;
        return true;
        end;
        """
        LEXER.input(test_input)
        output = [
            ("PROGRAM_KW", "program"),
            ("IDENTIFIER", "prg1"),
            ("SEMICOLON", ";"),
            ("INTEGER_KW", "integer"),
            ("IDENTIFIER", "num"),
            ("COMMA", ","),
            ("IDENTIFIER", "divisor"),
            ("COMMA", ","),
            ("IDENTIFIER", "quotient"),
            ("SEMICOLON", ";"),
            ("BEGIN_KW", "begin"),
            ("IDENTIFIER", "num"),
            ("ASSIGN_OP", ":="),
            ("NUMBER", "61"),
            ("SEMICOLON", ";"),
            ("IDENTIFIER", "divisor"),
            ("ASSIGN_OP", ":="),
            ("NUMBER", "2"),
            ("SEMICOLON", ";"),
            ("IDENTIFIER", "quotient"),
            ("ASSIGN_OP", ":="),
            ("NUMBER", "0"),
            ("SEMICOLON", ";"),
            ("IF_KW", "if"),
            ("IDENTIFIER", "num"),
            ("EQ_OP", "="),
            ("NUMBER", "1"),
            ("THEN_KW", "then"),
            ("RETURN_KW", "return"),
            ("FALSE_KW", "false"),
            ("SEMICOLON", ";"),
            ("ELSE_KW", "else"),
            ("IF_KW", "if"),
            ("IDENTIFIER", "num"),
            ("EQ_OP", "="),
            ("NUMBER", "2"),
            ("THEN_KW", "then"),
            ("RETURN_KW", "return"),
            ("TRUE_KW", "true"),
            ("SEMICOLON", ";"),
            ("WHILE_KW", "while"),
            ("IDENTIFIER", "divisor"),
            ("LE_OP", "<="),
            ("LEFT_PA", "("),
            ("IDENTIFIER", "num"),
            ("DIV_OP", "/"),
            ("NUMBER", "2"),
            ("RIGHT_PA", ")"),
            ("DO_KW", "do"),
            ("BEGIN_KW", "begin"),
            ("IDENTIFIER", "quotient"),
            ("ASSIGN_OP", ":="),
            ("IDENTIFIER", "num"),
            ("DIV_OP", "/"),
            ("IDENTIFIER", "divisor"),
            ("SEMICOLON", ";"),
            ("IF_KW", "if"),
            ("IDENTIFIER", "divisor"),
            ("MUL_OP", "*"),
            ("IDENTIFIER", "quotient"),
            ("EQ_OP", "="),
            ("IDENTIFIER", "num"),
            ("THEN_KW", "then"),
            ("RETURN_KW", "return"),
            ("FALSE_KW", "false"),
            ("SEMICOLON", ";"),
            ("IDENTIFIER", "divisor"),
            ("ASSIGN_OP", ":="),
            ("IDENTIFIER", "divisor"),
            ("ADD_OP", "+"),
            ("NUMBER", "1"),
            ("SEMICOLON", ";"),
            ("END_KW", "end"),
            ("SEMICOLON", ";"),
            ("RETURN_KW", "return"),
            ("TRUE_KW", "true"),
            ("SEMICOLON", ";"),
            ("END_KW", "end"),
            ("SEMICOLON", ";"),
        ]
        it = iter(output)
        for tok in LEXER:
            right_token = next(it)
            self.assertEqual(right_token, (tok.type, tok.value))

    def test2(self):
        test_input: str = """program prg2;
        function avg(integer m; integer n):real
        integer sum, num;
        real average;
        begin
        sum:=0;
        average:=0.0;
        for num:=m to n do
        sum:=sum+num;
        average:=sum/(n-m+1);
        return average;
        end;
        begin
        a:=avg(1,20);
        end;"""
        LEXER.input(test_input)
        output = [
            ("PROGRAM_KW", "program"),
            ("IDENTIFIER", "prg2"),
            ("SEMICOLON", ";"),
            ("FUNCTION_KW", "function"),
            ("IDENTIFIER", "avg"),
            ("LEFT_PA", "("),
            ("INTEGER_KW", "integer"),
            ("IDENTIFIER", "m"),
            ("SEMICOLON", ";"),
            ("INTEGER_KW", "integer"),
            ("IDENTIFIER", "n"),
            ("RIGHT_PA", ")"),
            ("COLON", ":"),
            ("REAL_KW", "real"),
            ("INTEGER_KW", "integer"),
            ("IDENTIFIER", "sum"),
            ("COMMA", ","),
            ("IDENTIFIER", "num"),
            ("SEMICOLON", ";"),
            ("REAL_KW", "real"),
            ("IDENTIFIER", "average"),
            ("SEMICOLON", ";"),
            ("BEGIN_KW", "begin"),
            ("IDENTIFIER", "sum"),
            ("ASSIGN_OP", ":="),
            ("NUMBER", "0"),
            ("SEMICOLON", ";"),
            ("IDENTIFIER", "average"),
            ("ASSIGN_OP", ":="),
            ("NUMBER", "0.0"),
            ("SEMICOLON", ";"),
            ("FOR_KW", "for"),
            ("IDENTIFIER", "num"),
            ("ASSIGN_OP", ":="),
            ("IDENTIFIER", "m"),
            ("TO_KW", "to"),
            ("IDENTIFIER", "n"),
            ("DO_KW", "do"),
            ("IDENTIFIER", "sum"),
            ("ASSIGN_OP", ":="),
            ("IDENTIFIER", "sum"),
            ("ADD_OP", "+"),
            ("IDENTIFIER", "num"),
            ("SEMICOLON", ";"),
            ("IDENTIFIER", "average"),
            ("ASSIGN_OP", ":="),
            ("IDENTIFIER", "sum"),
            ("DIV_OP", "/"),
            ("LEFT_PA", "("),
            ("IDENTIFIER", "n"),
            ("SUB_OP", "-"),
            ("IDENTIFIER", "m"),
            ("ADD_OP", "+"),
            ("NUMBER", "1"),
            ("RIGHT_PA", ")"),
            ("SEMICOLON", ";"),
            ("RETURN_KW", "return"),
            ("IDENTIFIER", "average"),
            ("SEMICOLON", ";"),
            ("END_KW", "end"),
            ("SEMICOLON", ";"),
            ("BEGIN_KW", "begin"),
            ("IDENTIFIER", "a"),
            ("ASSIGN_OP", ":="),
            ("IDENTIFIER", "avg"),
            ("LEFT_PA", "("),
            ("NUMBER", "1"),
            ("COMMA", ","),
            ("NUMBER", "20"),
            ("RIGHT_PA", ")"),
            ("SEMICOLON", ";"),
            ("END_KW", "end"),
            ("SEMICOLON", ";"),
        ]

        it = iter(output)

        for tok in LEXER:
            right_token = next(it)
            self.assertEqual(right_token, (tok.type, tok.value))

if __name__ == '__main__':
    unittest.main()
