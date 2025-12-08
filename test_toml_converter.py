from toml_converter import convert_to_toml, value_to_toml


def test_simple_number():
    data = {"x": 42}
    result = convert_to_toml(data)
    assert result == 'x = 42\n'


def test_simple_string():
    data = {"name": "hello"}
    result = convert_to_toml(data)
    assert result == 'name = "hello"\n'


def test_simple_array():
    data = {"arr": [1, 2, 3]}
    result = convert_to_toml(data)
    assert result == 'arr = [1, 2, 3]\n'


def test_array_of_strings():
    data = {"names": ["alice", "bob", "charlie"]}
    result = convert_to_toml(data)
    assert result == 'names = ["alice", "bob", "charlie"]\n'


def test_empty_array():
    data = {"arr": []}
    result = convert_to_toml(data)
    assert result == 'arr = []\n'


def test_multiple_simple_values():
    data = {
        "port": 8080,
        "host": "localhost",
        "debug": 1
    }
    result = convert_to_toml(data)
    lines = result.strip().split('\n')
    assert len(lines) == 3
    assert 'port = 8080' in result
    assert 'host = "localhost"' in result
    assert 'debug = 1' in result


def test_simple_table():
    data = {
        "config": {
            "host": "localhost",
            "port": 8080
        }
    }
    result = convert_to_toml(data)
    assert '[config]' in result
    assert 'host = "localhost"' in result
    assert 'port = 8080' in result


def test_nested_table():
    data = {
        "server": {
            "connection": {
                "host": "localhost",
                "port": 8080
            }
        }
    }
    result = convert_to_toml(data)
    assert '[server]' in result
    assert '[server.connection]' in result
    assert 'host = "localhost"' in result
    assert 'port = 8080' in result


def test_table_with_array():
    data = {
        "config": {
            "ports": [8080, 8081, 8082]
        }
    }
    result = convert_to_toml(data)
    assert '[config]' in result
    assert 'ports = [8080, 8081, 8082]' in result


def test_mixed_values_and_tables():
    data = {
        "port": 8080,
        "config": {
            "host": "localhost"
        }
    }
    result = convert_to_toml(data)
    assert 'port = 8080' in result
    assert '[config]' in result
    assert 'host = "localhost"' in result


def test_value_to_toml_int():
    assert value_to_toml(42) == "42"


def test_value_to_toml_string():
    assert value_to_toml("hello") == '"hello"'


def test_value_to_toml_array():
    assert value_to_toml([1, 2, 3]) == "[1, 2, 3]"


def test_value_to_toml_empty_array():
    assert value_to_toml([]) == "[]"


def test_value_to_toml_inline_table():
    result = value_to_toml({"a": 1, "b": 2})
    assert "a = 1" in result
    assert "b = 2" in result


def test_complex_structure():
    data = {
        "port": 8080,
        "host": "localhost",
        "database": {
            "name": "mydb",
            "pool": {
                "min": 5,
                "max": 20
            }
        }
    }
    result = convert_to_toml(data)
    assert 'port = 8080' in result
    assert 'host = "localhost"' in result
    assert '[database]' in result
    assert 'name = "mydb"' in result
    assert '[database.pool]' in result
    assert 'min = 5' in result
    assert 'max = 20' in result


def test_empty_dict():
    data = {"empty": {}}
    result = convert_to_toml(data)
    assert 'empty = {}' in result


def test_array_mixed_types():
    data = {"mixed": [1, "hello", 2, "world"]}
    result = convert_to_toml(data)
    assert 'mixed = [1, "hello", 2, "world"]' in result
