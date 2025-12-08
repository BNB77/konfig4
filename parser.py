from dataclasses import dataclass
from typing import List, Union, Dict, Any
from lexer import Token, TokenType, Lexer


class ParserError(Exception):
    def __init__(self, message: str, token: Token):
        self.message = message
        self.token = token
        super().__init__(f"Ошибка на строке {token.line}, столбец {token.column}: {message}")


@dataclass
class NumberNode:
    value: int


@dataclass
class NameNode:
    name: str


@dataclass
class ArrayNode:
    elements: List[Any]


@dataclass
class DictNode:
    pairs: Dict[str, Any]


@dataclass
class ConstEvalNode:
    name: str


@dataclass
class SetStatementNode:
    name: str
    value: Any


@dataclass
class ProgramNode:
    statements: List[SetStatementNode]


class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0

    def current_token(self) -> Token:
        if self.pos >= len(self.tokens):
            return self.tokens[-1]
        return self.tokens[self.pos]

    def peek_token(self, offset: int = 1) -> Token:
        pos = self.pos + offset
        if pos >= len(self.tokens):
            return self.tokens[-1]
        return self.tokens[pos]

    def advance(self):
        if self.pos < len(self.tokens):
            self.pos += 1

    def expect(self, token_type: TokenType) -> Token:
        token = self.current_token()
        if token.type != token_type:
            raise ParserError(f"Ожидался {token_type.name}, получен {token.type.name}", token)
        self.advance()
        return token

    def parse_value(self) -> Union[NumberNode, NameNode, ArrayNode, DictNode, ConstEvalNode]:
        token = self.current_token()

        if token.type == TokenType.NUMBER:
            self.advance()
            return NumberNode(value=token.value)

        if token.type == TokenType.NAME:
            self.advance()
            return NameNode(name=token.value)

        if token.type == TokenType.LBRACE:
            return self.parse_array()

        if token.type == TokenType.LBRACKET:
            return self.parse_dict()

        if token.type == TokenType.HASH:
            return self.parse_const_eval()

        raise ParserError(f"Неожиданный токен {token.type.name}", token)

    def parse_array(self) -> ArrayNode:
        self.expect(TokenType.LBRACE)
        elements = []

        while self.current_token().type != TokenType.RBRACE:
            if self.current_token().type == TokenType.EOF:
                raise ParserError("Незакрытый массив", self.current_token())

            elements.append(self.parse_value())

            if self.current_token().type == TokenType.COMMA:
                self.advance()
            elif self.current_token().type != TokenType.RBRACE:
                raise ParserError("Ожидалась запятая или закрывающая скобка", self.current_token())

        self.expect(TokenType.RBRACE)
        return ArrayNode(elements=elements)

    def parse_dict(self) -> DictNode:
        self.expect(TokenType.LBRACKET)
        pairs = {}

        while self.current_token().type != TokenType.RBRACKET:
            if self.current_token().type == TokenType.EOF:
                raise ParserError("Незакрытый словарь", self.current_token())

            key_token = self.expect(TokenType.NAME)
            key = key_token.value

            self.expect(TokenType.ARROW)

            value = self.parse_value()
            pairs[key] = value

            if self.current_token().type == TokenType.COMMA:
                self.advance()
            elif self.current_token().type != TokenType.RBRACKET:
                raise ParserError("Ожидалась запятая или закрывающая скобка", self.current_token())

        self.expect(TokenType.RBRACKET)
        return DictNode(pairs=pairs)

    def parse_const_eval(self) -> ConstEvalNode:
        self.expect(TokenType.HASH)
        self.expect(TokenType.LPAREN)
        name_token = self.expect(TokenType.NAME)
        self.expect(TokenType.RPAREN)
        return ConstEvalNode(name=name_token.value)

    def parse_set_statement(self) -> SetStatementNode:
        self.expect(TokenType.SET)
        name_token = self.expect(TokenType.NAME)
        self.expect(TokenType.EQUAL)
        value = self.parse_value()
        return SetStatementNode(name=name_token.value, value=value)

    def parse_program(self) -> ProgramNode:
        statements = []

        while self.current_token().type != TokenType.EOF:
            if self.current_token().type == TokenType.SET:
                statements.append(self.parse_set_statement())
            else:
                raise ParserError(f"Неожиданный токен {self.current_token().type.name}", self.current_token())

        return ProgramNode(statements=statements)


def parse(text: str) -> ProgramNode:
    lexer = Lexer(text)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    return parser.parse_program()
