from interpreter import interpret, InterpreterError
from parser import ParserError
from lexer import LexerError
import sys
import json


def main():
    if len(sys.argv) < 2:
        print("Использование: python demo_interpreter.py <файл>")
        sys.exit(1)

    filename = sys.argv[1]

    try:
        with open(filename, 'r', encoding='utf-8') as f:
            text = f.read()

        result = interpret(text)

        print("=== Результат интерпретации ===\n")
        print(json.dumps(result, indent=2, ensure_ascii=False))

    except LexerError as e:
        print(f"Ошибка лексера: {e}")
        sys.exit(1)
    except ParserError as e:
        print(f"Ошибка парсера: {e}")
        sys.exit(1)
    except InterpreterError as e:
        print(f"Ошибка интерпретатора: {e}")
        sys.exit(1)
    except FileNotFoundError:
        print(f"Файл '{filename}' не найден")
        sys.exit(1)
    except Exception as e:
        print(f"Ошибка: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
