import pytest
from interpreter import interpret, InterpreterError


def test_simple_number():
    result = interpret("set x = 42")
    assert result["x"] == 42


def test_simple_name():
    result = interpret("set x = hello")
    assert result["x"] == "hello"


def test_simple_array():
    result = interpret("set arr = { 1, 2, 3 }")
    assert result["arr"] == [1, 2, 3]


def test_simple_dict():
    result = interpret("set cfg = [ a => 1, b => 2 ]")
    assert result["cfg"] == {"a": 1, "b": 2}


def test_const_evaluation():
    result = interpret("""
        set x = 10
        set y = #(x)
    """)
    assert result["x"] == 10
    assert result["y"] == 10


def test_const_eval_in_array():
    result = interpret("""
        set base = 100
        set arr = { 1, #(base), 3 }
    """)
    assert result["arr"] == [1, 100, 3]


def test_const_eval_in_dict():
    result = interpret("""
        set port = 8080
        set cfg = [ server => localhost, port => #(port) ]
    """)
    assert result["cfg"] == {"server": "localhost", "port": 8080}


def test_nested_array():
    result = interpret("set arr = { 1, { 2, 3 }, 4 }")
    assert result["arr"] == [1, [2, 3], 4]


def test_nested_dict():
    result = interpret("""
        set cfg = [
            db => [ host => localhost, port => 5432 ],
            cache => [ enabled => true ]
        ]
    """)
    assert result["cfg"]["db"] == {"host": "localhost", "port": 5432}
    assert result["cfg"]["cache"] == {"enabled": "true"}


def test_array_with_names():
    result = interpret("set users = { alice, bob, charlie }")
    assert result["users"] == ["alice", "bob", "charlie"]


def test_multiple_statements():
    result = interpret("""
        set a = 1
        set b = 2
        set c = 3
    """)
    assert result["a"] == 1
    assert result["b"] == 2
    assert result["c"] == 3


def test_const_eval_array():
    result = interpret("""
        set arr = { 1, 2, 3 }
        set copy = #(arr)
    """)
    assert result["copy"] == [1, 2, 3]


def test_const_eval_dict():
    result = interpret("""
        set cfg = [ a => 1, b => 2 ]
        set copy = #(cfg)
    """)
    assert result["copy"] == {"a": 1, "b": 2}


def test_chained_const_eval():
    result = interpret("""
        set x = 10
        set y = #(x)
        set z = #(y)
    """)
    assert result["x"] == 10
    assert result["y"] == 10
    assert result["z"] == 10


def test_const_eval_nested():
    result = interpret("""
        set inner = { 1, 2, 3 }
        set outer = { #(inner), 4 }
    """)
    assert result["outer"] == [[1, 2, 3], 4]


def test_undefined_const_error():
    with pytest.raises(InterpreterError):
        interpret("set x = #(undefined)")


def test_forward_reference_error():
    with pytest.raises(InterpreterError):
        interpret("""
            set x = #(y)
            set y = 10
        """)


def test_empty_array():
    result = interpret("set arr = { }")
    assert result["arr"] == []


def test_empty_dict():
    result = interpret("set cfg = [ ]")
    assert result["cfg"] == {}


def test_complex_nested_structure():
    result = interpret("""
        set port = 8080
        set host = localhost
        set config = [
            server => [
                host => #(host),
                port => #(port),
                endpoints => { api, admin, health }
            ],
            database => [
                connections => { 1, 5, 10, 20 }
            ]
        ]
    """)
    assert result["config"]["server"]["host"] == "localhost"
    assert result["config"]["server"]["port"] == 8080
    assert result["config"]["server"]["endpoints"] == ["api", "admin", "health"]
    assert result["config"]["database"]["connections"] == [1, 5, 10, 20]


def test_overwrite_constant():
    result = interpret("""
        set x = 10
        set x = 20
    """)
    assert result["x"] == 20


def test_const_eval_in_nested_dict():
    result = interpret("""
        set timeout = 30
        set cfg = [
            level1 => [
                level2 => [
                    timeout => #(timeout)
                ]
            ]
        ]
    """)
    assert result["cfg"]["level1"]["level2"]["timeout"] == 30


def test_mixed_types_in_array():
    result = interpret("set mixed = { 1, hello, { 2, 3 }, world }")
    assert result["mixed"] == [1, "hello", [2, 3], "world"]


def test_mixed_types_in_dict():
    result = interpret("""
        set data = [
            num => 42,
            name => test,
            list => { 1, 2, 3 }
        ]
    """)
    assert result["data"]["num"] == 42
    assert result["data"]["name"] == "test"
    assert result["data"]["list"] == [1, 2, 3]
