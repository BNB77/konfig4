from typing import Any, Dict, List, Union


def value_to_toml(value: Any, indent: int = 0) -> str:
    if isinstance(value, int):
        return str(value)

    if isinstance(value, str):
        return f'"{value}"'

    if isinstance(value, list):
        if not value:
            return "[]"

        if all(isinstance(v, (int, str)) for v in value):
            elements = [value_to_toml(v) for v in value]
            return f"[{', '.join(elements)}]"

        result = "[\n"
        for item in value:
            result += "  " * (indent + 1) + value_to_toml(item, indent + 1) + ",\n"
        result += "  " * indent + "]"
        return result

    if isinstance(value, dict):
        if not value:
            return "{}"

        if all(isinstance(v, (int, str)) for v in value.values()):
            pairs = [f"{k} = {value_to_toml(v)}" for k, v in value.items()]
            return f"{{ {', '.join(pairs)} }}"

        result = "{\n"
        for k, v in value.items():
            result += "  " * (indent + 1) + f"{k} = {value_to_toml(v, indent + 1)},\n"
        result += "  " * indent + "}"
        return result

    return str(value)


def is_table(value: Any) -> bool:
    return isinstance(value, dict) and value


def convert_to_toml(data: Dict[str, Any]) -> str:
    lines = []
    simple_values = {}
    tables = {}

    for key, value in data.items():
        if is_table(value):
            tables[key] = value
        else:
            simple_values[key] = value

    for key, value in simple_values.items():
        lines.append(f"{key} = {value_to_toml(value)}")

    if simple_values and tables:
        lines.append("")

    for table_name, table_value in tables.items():
        lines.append(f"[{table_name}]")

        if isinstance(table_value, dict):
            simple_in_table = {}
            nested_tables = {}

            for key, value in table_value.items():
                if isinstance(value, dict) and value:
                    nested_tables[key] = value
                else:
                    simple_in_table[key] = value

            for key, value in simple_in_table.items():
                lines.append(f"{key} = {value_to_toml(value)}")

            for nested_name, nested_value in nested_tables.items():
                if simple_in_table:
                    lines.append("")
                lines.append(f"[{table_name}.{nested_name}]")
                if isinstance(nested_value, dict):
                    for key, value in nested_value.items():
                        lines.append(f"{key} = {value_to_toml(value)}")

        lines.append("")

    result = "\n".join(lines)
    return result.rstrip() + "\n"
