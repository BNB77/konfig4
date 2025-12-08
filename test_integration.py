import subprocess
import tempfile
import os


def run_config_tool(input_text):
    with tempfile.NamedTemporaryFile(mode='w', suffix='.conf', delete=False, encoding='utf-8') as f:
        f.write(input_text)
        temp_file = f.name

    try:
        result = subprocess.run(
            ['python', 'config_tool.py', temp_file],
            capture_output=True,
            text=True,
            timeout=5
        )
        return result.stdout, result.stderr, result.returncode
    finally:
        os.unlink(temp_file)


def test_simple_config():
    input_text = """
    set port = 8080
    set host = localhost
    """
    stdout, stderr, code = run_config_tool(input_text)
    assert code == 0
    assert 'port = 8080' in stdout
    assert 'host = "localhost"' in stdout


def test_array_config():
    input_text = """
    set numbers = { 1, 2, 3, 4, 5 }
    """
    stdout, stderr, code = run_config_tool(input_text)
    assert code == 0
    assert 'numbers = [1, 2, 3, 4, 5]' in stdout


def test_dict_config():
    input_text = """
    set config = [ host => localhost, port => 8080 ]
    """
    stdout, stderr, code = run_config_tool(input_text)
    assert code == 0
    assert '[config]' in stdout
    assert 'host = "localhost"' in stdout
    assert 'port = 8080' in stdout


def test_const_evaluation():
    input_text = """
    set base_port = 8080
    set server_port = #(base_port)
    """
    stdout, stderr, code = run_config_tool(input_text)
    assert code == 0
    assert 'base_port = 8080' in stdout
    assert 'server_port = 8080' in stdout


def test_nested_structures():
    input_text = """
    set config = [
        server => [ host => localhost, port => 8080 ],
        database => [ name => mydb, connections => 10 ]
    ]
    """
    stdout, stderr, code = run_config_tool(input_text)
    assert code == 0
    assert '[config]' in stdout
    assert '[config.server]' in stdout
    assert '[config.database]' in stdout


def test_comments_ignored():
    input_text = """
    *> This is a comment
    set x = 42
    *> Another comment
    set y = 100
    """
    stdout, stderr, code = run_config_tool(input_text)
    assert code == 0
    assert 'x = 42' in stdout
    assert 'y = 100' in stdout


def test_syntax_error():
    input_text = """
    set x = @invalid
    """
    stdout, stderr, code = run_config_tool(input_text)
    assert code != 0
    assert 'Синтаксическая ошибка' in stderr


def test_undefined_constant():
    input_text = """
    set x = #(undefined)
    """
    stdout, stderr, code = run_config_tool(input_text)
    assert code != 0
    assert 'Ошибка выполнения' in stderr


def test_complex_example():
    input_text = """
    *> Server configuration

    set default_port = 8080
    set default_host = localhost

    set primary = [
        host => #(default_host),
        port => #(default_port),
        timeout => 30
    ]

    set allowed_methods = { GET, POST, PUT, DELETE }

    set server_config = [
        primary => #(primary),
        methods => #(allowed_methods)
    ]
    """
    stdout, stderr, code = run_config_tool(input_text)
    assert code == 0
    assert 'default_port = 8080' in stdout
    assert 'default_host = "localhost"' in stdout
    assert '[primary]' in stdout
    assert 'allowed_methods = ["GET", "POST", "PUT", "DELETE"]' in stdout


def test_empty_structures():
    input_text = """
    set empty_array = { }
    set empty_dict = [ ]
    """
    stdout, stderr, code = run_config_tool(input_text)
    assert code == 0
    assert 'empty_array = []' in stdout
    assert 'empty_dict = {}' in stdout


def test_multiple_const_eval():
    input_text = """
    set a = 10
    set b = #(a)
    set c = #(b)
    set d = #(c)
    """
    stdout, stderr, code = run_config_tool(input_text)
    assert code == 0
    assert 'a = 10' in stdout
    assert 'b = 10' in stdout
    assert 'c = 10' in stdout
    assert 'd = 10' in stdout


def test_example1_file():
    result = subprocess.run(
        ['python', 'config_tool.py', 'example1.conf'],
        capture_output=True,
        text=True,
        timeout=5
    )
    assert result.returncode == 0
    assert 'port = 8080' in result.stdout
    assert 'host = "localhost"' in result.stdout
    assert 'numbers = [10, 20, 30, 40, 50]' in result.stdout


def test_example2_file():
    result = subprocess.run(
        ['python', 'config_tool.py', 'example2.conf'],
        capture_output=True,
        text=True,
        timeout=5
    )
    assert result.returncode == 0
    assert 'db_host = "localhost"' in result.stdout
    assert 'db_port = 5432' in result.stdout


def test_example3_file():
    result = subprocess.run(
        ['python', 'config_tool.py', 'example3.conf'],
        capture_output=True,
        text=True,
        timeout=5
    )
    assert result.returncode == 0
    assert 'default_port = 8080' in result.stdout
    assert '[primary_server]' in result.stdout
    assert '[backup_server]' in result.stdout
