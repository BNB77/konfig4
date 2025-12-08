from typing import Any, Dict, Union, List
from parser import (
    ProgramNode, SetStatementNode, NumberNode, NameNode,
    ArrayNode, DictNode, ConstEvalNode, parse
)


class InterpreterError(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class Interpreter:
    def __init__(self):
        self.constants: Dict[str, Any] = {}

    def eval_value(self, node: Any) -> Any:
        if isinstance(node, NumberNode):
            return node.value

        if isinstance(node, NameNode):
            return node.name

        if isinstance(node, ArrayNode):
            return [self.eval_value(elem) for elem in node.elements]

        if isinstance(node, DictNode):
            result = {}
            for key, value in node.pairs.items():
                result[key] = self.eval_value(value)
            return result

        if isinstance(node, ConstEvalNode):
            if node.name not in self.constants:
                raise InterpreterError(f"Константа '{node.name}' не определена")
            return self.constants[node.name]

        raise InterpreterError(f"Неизвестный тип узла: {type(node).__name__}")

    def eval_statement(self, stmt: SetStatementNode):
        value = self.eval_value(stmt.value)
        self.constants[stmt.name] = value

    def eval_program(self, program: ProgramNode) -> Dict[str, Any]:
        for stmt in program.statements:
            self.eval_statement(stmt)
        return self.constants


def interpret(text: str) -> Dict[str, Any]:
    ast = parse(text)
    interpreter = Interpreter()
    return interpreter.eval_program(ast)
