from lexer import Lexer, LexerError
import sys


def main():
    if len(sys.argv) < 2:
        print("Использование: python demo_lexer.py <файл>")
        sys.exit(1)

    filename = sys.argv[1]

    try:
        with open(filename, 'r', encoding='utf-8') as f:
            text = f.read()

        lexer = Lexer(text)
        tokens = lexer.tokenize()

        print(f"Всего токенов: {len(tokens)}\n")

        for i, token in enumerate(tokens):
            if token.type.name == 'EOF':
                print(f"{i}: {token.type.name}")
            else:
                print(f"{i}: {token.type.name:15} | {token.value:20} | Строка {token.line}, Столбец {token.column}")

    except LexerError as e:
        print(f"Ошибка лексера: {e}")
        sys.exit(1)
    except FileNotFoundError:
        print(f"Файл '{filename}' не найден")
        sys.exit(1)
    except Exception as e:
        print(f"Ошибка: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
