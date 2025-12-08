import pytest
from parser import (
    parse, Parser, ParserError,
    NumberNode, NameNode, ArrayNode, DictNode, ConstEvalNode,
    SetStatementNode, ProgramNode
)
from lexer import Lexer


def test_parse_number():
    result = parse("set x = 42")
    assert len(result.statements) == 1
    assert result.statements[0].name == "x"
    assert isinstance(result.statements[0].value, NumberNode)
    assert result.statements[0].value.value == 42


def test_parse_name():
    result = parse("set x = myname")
    assert len(result.statements) == 1
    assert result.statements[0].name == "x"
    assert isinstance(result.statements[0].value, NameNode)
    assert result.statements[0].value.name == "myname"


def test_parse_simple_array():
    result = parse("set arr = { 1, 2, 3 }")
    assert len(result.statements) == 1
    stmt = result.statements[0]
    assert stmt.name == "arr"
    assert isinstance(stmt.value, ArrayNode)
    assert len(stmt.value.elements) == 3
    assert stmt.value.elements[0].value == 1
    assert stmt.value.elements[1].value == 2
    assert stmt.value.elements[2].value == 3


def test_parse_nested_array():
    result = parse("set arr = { 1, { 2, 3 }, 4 }")
    assert len(result.statements) == 1
    stmt = result.statements[0]
    assert isinstance(stmt.value, ArrayNode)
    assert len(stmt.value.elements) == 3
    assert isinstance(stmt.value.elements[1], ArrayNode)
    assert len(stmt.value.elements[1].elements) == 2


def test_parse_simple_dict():
    result = parse("set cfg = [ a => 1, b => 2 ]")
    assert len(result.statements) == 1
    stmt = result.statements[0]
    assert stmt.name == "cfg"
    assert isinstance(stmt.value, DictNode)
    assert len(stmt.value.pairs) == 2
    assert isinstance(stmt.value.pairs["a"], NumberNode)
    assert stmt.value.pairs["a"].value == 1
    assert isinstance(stmt.value.pairs["b"], NumberNode)
    assert stmt.value.pairs["b"].value == 2


def test_parse_dict_with_array():
    result = parse("set cfg = [ items => { 1, 2, 3 }, count => 3 ]")
    assert len(result.statements) == 1
    stmt = result.statements[0]
    assert isinstance(stmt.value, DictNode)
    assert isinstance(stmt.value.pairs["items"], ArrayNode)
    assert len(stmt.value.pairs["items"].elements) == 3
    assert isinstance(stmt.value.pairs["count"], NumberNode)


def test_parse_const_eval():
    result = parse("set y = #(x)")
    assert len(result.statements) == 1
    stmt = result.statements[0]
    assert stmt.name == "y"
    assert isinstance(stmt.value, ConstEvalNode)
    assert stmt.value.name == "x"


def test_parse_multiple_statements():
    text = """
    set x = 10
    set y = 20
    set z = 30
    """
    result = parse(text)
    assert len(result.statements) == 3
    assert result.statements[0].name == "x"
    assert result.statements[1].name == "y"
    assert result.statements[2].name == "z"


def test_parse_empty_array():
    result = parse("set arr = { }")
    assert len(result.statements) == 1
    stmt = result.statements[0]
    assert isinstance(stmt.value, ArrayNode)
    assert len(stmt.value.elements) == 0


def test_parse_empty_dict():
    result = parse("set cfg = [ ]")
    assert len(result.statements) == 1
    stmt = result.statements[0]
    assert isinstance(stmt.value, DictNode)
    assert len(stmt.value.pairs) == 0


def test_parse_complex_nested():
    text = """
    set config = [
        server => [ host => localhost, port => 8080 ],
        data => { 1, 2, { 3, 4 } }
    ]
    """
    result = parse(text)
    assert len(result.statements) == 1
    stmt = result.statements[0]
    assert isinstance(stmt.value, DictNode)
    assert isinstance(stmt.value.pairs["server"], DictNode)
    assert isinstance(stmt.value.pairs["data"], ArrayNode)


def test_unclosed_array_error():
    with pytest.raises(ParserError):
        parse("set x = { 1, 2")


def test_unclosed_dict_error():
    with pytest.raises(ParserError):
        parse("set x = [ a => 1")


def test_missing_arrow_in_dict():
    with pytest.raises(ParserError):
        parse("set x = [ a 1 ]")


def test_missing_equal_sign():
    with pytest.raises(ParserError):
        parse("set x 42")


def test_unexpected_token():
    with pytest.raises(ParserError):
        parse("x = 42")


def test_missing_comma_in_array():
    with pytest.raises(ParserError):
        parse("set x = { 1 2 3 }")


def test_missing_comma_in_dict():
    with pytest.raises(ParserError):
        parse("set x = [ a => 1 b => 2 ]")


def test_trailing_comma_array():
    result = parse("set x = { 1, 2, 3, }")
    assert len(result.statements) == 1
    stmt = result.statements[0]
    assert isinstance(stmt.value, ArrayNode)
    assert len(stmt.value.elements) == 3


def test_trailing_comma_dict():
    result = parse("set x = [ a => 1, b => 2, ]")
    assert len(result.statements) == 1
    stmt = result.statements[0]
    assert isinstance(stmt.value, DictNode)
    assert len(stmt.value.pairs) == 2


def test_dict_with_name_values():
    result = parse("set cfg = [ host => localhost, user => admin ]")
    assert len(result.statements) == 1
    stmt = result.statements[0]
    assert isinstance(stmt.value, DictNode)
    assert isinstance(stmt.value.pairs["host"], NameNode)
    assert stmt.value.pairs["host"].name == "localhost"


def test_array_with_names():
    result = parse("set users = { alice, bob, charlie }")
    assert len(result.statements) == 1
    stmt = result.statements[0]
    assert isinstance(stmt.value, ArrayNode)
    assert all(isinstance(el, NameNode) for el in stmt.value.elements)
    assert stmt.value.elements[0].name == "alice"


def test_const_eval_in_array():
    result = parse("set arr = { 1, #(x), 3 }")
    assert len(result.statements) == 1
    stmt = result.statements[0]
    assert isinstance(stmt.value, ArrayNode)
    assert isinstance(stmt.value.elements[1], ConstEvalNode)
    assert stmt.value.elements[1].name == "x"


def test_const_eval_in_dict():
    result = parse("set cfg = [ value => #(myconst) ]")
    assert len(result.statements) == 1
    stmt = result.statements[0]
    assert isinstance(stmt.value, DictNode)
    assert isinstance(stmt.value.pairs["value"], ConstEvalNode)
