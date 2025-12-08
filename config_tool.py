#!/usr/bin/env python3

import sys

from interpreter import interpret, InterpreterError
from parser import ParserError
from lexer import LexerError
from toml_converter import convert_to_toml


def main():
    if len(sys.argv) < 2:
        print("Использование: config_tool.py <входной_файл>", file=sys.stderr)
        sys.exit(1)

    input_file = sys.argv[1]

    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            text = f.read()

        constants = interpret(text)
        toml_output = convert_to_toml(constants)
        print(toml_output, end='')

    except FileNotFoundError:
        print(f"Ошибка: файл '{input_file}' не найден", file=sys.stderr)
        sys.exit(1)
    except LexerError as e:
        print(f"Синтаксическая ошибка: {e}", file=sys.stderr)
        sys.exit(1)
    except ParserError as e:
        print(f"Синтаксическая ошибка: {e}", file=sys.stderr)
        sys.exit(1)
    except InterpreterError as e:
        print(f"Ошибка выполнения: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Неожиданная ошибка: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
