from unittest import TestCase, main
from lexer import LEXER

from parser import PARSER


class ParserTest(TestCase):
    def test1(self):
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
        # TODO: do the check
        PARSER.parse(test_input, LEXER)

    def test2(self):
        test_input = """program prg2;
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
        PARSER.parse(test_input, LEXER)

    def test_syntax_error_not_EOF(self):
        test_input = """program badTest;
        integer x;
        begin
        if num = 1 return false;
        return true;
        end;
        """
        PARSER.parse(test_input, LEXER)

    def test_syntax_error_EOF(self):  # TODO: this is probably not correct.
        test_input = """program badTestEOF;
        integer x,y;
        begin
        return 1 + 2 - 4 * 100;
        end"""
        PARSER.parse(test_input, LEXER)


if __name__ == "__main__":
    main()
