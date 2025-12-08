import pytest
from lexer import Lexer, TokenType, LexerError


def test_numbers():
    lexer = Lexer("123 456 789")
    tokens = lexer.tokenize()

    assert len(tokens) == 4
    assert tokens[0].type == TokenType.NUMBER
    assert tokens[0].value == 123
    assert tokens[1].type == TokenType.NUMBER
    assert tokens[1].value == 456
    assert tokens[2].type == TokenType.NUMBER
    assert tokens[2].value == 789
    assert tokens[3].type == TokenType.EOF


def test_number_cannot_start_with_zero():
    lexer = Lexer("0123")
    with pytest.raises(LexerError):
        lexer.tokenize()


def test_names():
    lexer = Lexer("abc def_ghi xyz123")
    tokens = lexer.tokenize()

    assert len(tokens) == 4
    assert tokens[0].type == TokenType.NAME
    assert tokens[0].value == "abc"
    assert tokens[1].type == TokenType.NAME
    assert tokens[1].value == "def_ghi"
    assert tokens[2].type == TokenType.NAME
    assert tokens[2].value == "xyz123"


def test_set_keyword():
    lexer = Lexer("set x = 5")
    tokens = lexer.tokenize()

    assert tokens[0].type == TokenType.SET
    assert tokens[1].type == TokenType.NAME
    assert tokens[1].value == "x"
    assert tokens[2].type == TokenType.EQUAL
    assert tokens[3].type == TokenType.NUMBER
    assert tokens[3].value == 5


def test_array():
    lexer = Lexer("{ 1, 2, 3 }")
    tokens = lexer.tokenize()

    assert tokens[0].type == TokenType.LBRACE
    assert tokens[1].type == TokenType.NUMBER
    assert tokens[2].type == TokenType.COMMA
    assert tokens[3].type == TokenType.NUMBER
    assert tokens[4].type == TokenType.COMMA
    assert tokens[5].type == TokenType.NUMBER
    assert tokens[6].type == TokenType.RBRACE


def test_dictionary():
    lexer = Lexer("[ a => 1, b => 2 ]")
    tokens = lexer.tokenize()

    assert tokens[0].type == TokenType.LBRACKET
    assert tokens[1].type == TokenType.NAME
    assert tokens[1].value == "a"
    assert tokens[2].type == TokenType.ARROW
    assert tokens[3].type == TokenType.NUMBER
    assert tokens[4].type == TokenType.COMMA
    assert tokens[5].type == TokenType.NAME
    assert tokens[5].value == "b"
    assert tokens[6].type == TokenType.ARROW
    assert tokens[7].type == TokenType.NUMBER
    assert tokens[8].type == TokenType.RBRACKET


def test_constant_evaluation():
    lexer = Lexer("#(myvar)")
    tokens = lexer.tokenize()

    assert tokens[0].type == TokenType.HASH
    assert tokens[1].type == TokenType.LPAREN
    assert tokens[2].type == TokenType.NAME
    assert tokens[2].value == "myvar"
    assert tokens[3].type == TokenType.RPAREN


def test_comments():
    lexer = Lexer("*> This is a comment\n123")
    tokens = lexer.tokenize()

    assert tokens[0].type == TokenType.NUMBER
    assert tokens[0].value == 123


def test_multiline():
    text = """set x = 5
set y = 10
set z = { 1, 2, 3 }"""
    lexer = Lexer(text)
    tokens = lexer.tokenize()

    assert tokens[0].type == TokenType.SET
    assert tokens[1].value == "x"
    assert tokens[3].value == 5

    assert tokens[4].type == TokenType.SET
    assert tokens[5].value == "y"
    assert tokens[7].value == 10


def test_nested_structures():
    lexer = Lexer("{ 1, { 2, 3 }, 4 }")
    tokens = lexer.tokenize()

    assert tokens[0].type == TokenType.LBRACE
    assert tokens[1].type == TokenType.NUMBER
    assert tokens[3].type == TokenType.LBRACE
    assert tokens[4].type == TokenType.NUMBER
    assert tokens[7].type == TokenType.RBRACE
    assert tokens[10].type == TokenType.RBRACE


def test_invalid_character():
    lexer = Lexer("@invalid")
    with pytest.raises(LexerError):
        lexer.tokenize()


def test_empty_input():
    lexer = Lexer("")
    tokens = lexer.tokenize()

    assert len(tokens) == 1
    assert tokens[0].type == TokenType.EOF


def test_whitespace_handling():
    lexer = Lexer("   123   \n\n  456  \t  789   ")
    tokens = lexer.tokenize()

    assert len(tokens) == 4
    assert tokens[0].value == 123
    assert tokens[1].value == 456
    assert tokens[2].value == 789


def test_complex_expression():
    text = """set data = [
    name => user123,
    values => { 10, 20, 30 },
    count => 3
]"""
    lexer = Lexer(text)
    tokens = lexer.tokenize()

    assert tokens[0].type == TokenType.SET
    assert tokens[1].value == "data"
    assert tokens[2].type == TokenType.EQUAL
    assert tokens[3].type == TokenType.LBRACKET
