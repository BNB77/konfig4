from parser import parse, ParserError
from lexer import LexerError
import sys
import json


def ast_to_dict(node):
    if hasattr(node, '__dataclass_fields__'):
        result = {'_type': node.__class__.__name__}
        for field_name in node.__dataclass_fields__:
            field_value = getattr(node, field_name)
            if isinstance(field_value, list):
                result[field_name] = [ast_to_dict(item) for item in field_value]
            elif isinstance(field_value, dict):
                result[field_name] = {k: ast_to_dict(v) for k, v in field_value.items()}
            else:
                result[field_name] = ast_to_dict(field_value) if hasattr(field_value, '__dataclass_fields__') else field_value
        return result
    return node


def print_ast(node, indent=0):
    prefix = "  " * indent

    if hasattr(node, '__dataclass_fields__'):
        print(f"{prefix}{node.__class__.__name__}:")
        for field_name in node.__dataclass_fields__:
            field_value = getattr(node, field_name)
            print(f"{prefix}  {field_name}:", end="")

            if isinstance(field_value, list):
                print()
                for item in field_value:
                    print_ast(item, indent + 2)
            elif isinstance(field_value, dict):
                print()
                for k, v in field_value.items():
                    print(f"{prefix}    {k}:", end="")
                    if hasattr(v, '__dataclass_fields__'):
                        print()
                        print_ast(v, indent + 3)
                    else:
                        print(f" {v}")
            elif hasattr(field_value, '__dataclass_fields__'):
                print()
                print_ast(field_value, indent + 2)
            else:
                print(f" {field_value}")
    else:
        print(f"{prefix}{node}")


def main():
    if len(sys.argv) < 2:
        print("Использование: python demo_parser.py <файл> [--json]")
        sys.exit(1)

    filename = sys.argv[1]
    output_json = "--json" in sys.argv

    try:
        with open(filename, 'r', encoding='utf-8') as f:
            text = f.read()

        ast = parse(text)

        if output_json:
            print(json.dumps(ast_to_dict(ast), indent=2, ensure_ascii=False))
        else:
            print("=== AST ===\n")
            print_ast(ast)

    except LexerError as e:
        print(f"Ошибка лексера: {e}")
        sys.exit(1)
    except ParserError as e:
        print(f"Ошибка парсера: {e}")
        sys.exit(1)
    except FileNotFoundError:
        print(f"Файл '{filename}' не найден")
        sys.exit(1)
    except Exception as e:
        print(f"Ошибка: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
