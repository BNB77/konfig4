import re
from enum import Enum, auto
from dataclasses import dataclass
from typing import List, Optional


class TokenType(Enum):
    NUMBER = auto()
    NAME = auto()
    LBRACE = auto()
    RBRACE = auto()
    LBRACKET = auto()
    RBRACKET = auto()
    ARROW = auto()
    COMMA = auto()
    SET = auto()
    EQUAL = auto()
    HASH = auto()
    LPAREN = auto()
    RPAREN = auto()
    COMMENT = auto()
    EOF = auto()


@dataclass
class Token:
    type: TokenType
    value: any
    line: int
    column: int


class LexerError(Exception):
    def __init__(self, message: str, line: int, column: int):
        self.message = message
        self.line = line
        self.column = column
        super().__init__(f"Ошибка на строке {line}, столбец {column}: {message}")


class Lexer:
    def __init__(self, text: str):
        self.text = text
        self.pos = 0
        self.line = 1
        self.column = 1
        self.tokens: List[Token] = []

    def current_char(self) -> Optional[str]:
        if self.pos >= len(self.text):
            return None
        return self.text[self.pos]

    def peek_char(self, offset: int = 1) -> Optional[str]:
        pos = self.pos + offset
        if pos >= len(self.text):
            return None
        return self.text[pos]

    def advance(self):
        if self.pos < len(self.text) and self.text[self.pos] == '\n':
            self.line += 1
            self.column = 1
        else:
            self.column += 1
        self.pos += 1

    def skip_whitespace(self):
        while self.current_char() and self.current_char() in ' \t\n\r':
            self.advance()

    def read_comment(self):
        start_line = self.line
        start_column = self.column

        if self.current_char() == '*' and self.peek_char() == '>':
            self.advance()
            self.advance()

            comment_text = ''
            while self.current_char() and self.current_char() != '\n':
                comment_text += self.current_char()
                self.advance()

            return Token(TokenType.COMMENT, comment_text.strip(), start_line, start_column)

        return None

    def read_number(self) -> Token:
        start_line = self.line
        start_column = self.column
        num_str = ''

        if self.current_char() == '0':
            raise LexerError("Число не может начинаться с 0", self.line, self.column)

        while self.current_char() and self.current_char().isdigit():
            num_str += self.current_char()
            self.advance()

        return Token(TokenType.NUMBER, int(num_str), start_line, start_column)

    def read_name(self) -> Token:
        start_line = self.line
        start_column = self.column
        name = ''

        while self.current_char() and (self.current_char().isalnum() or self.current_char() == '_'):
            name += self.current_char()
            self.advance()

        if name == 'set':
            return Token(TokenType.SET, name, start_line, start_column)

        return Token(TokenType.NAME, name, start_line, start_column)

    def tokenize(self) -> List[Token]:
        while self.current_char():
            self.skip_whitespace()

            if not self.current_char():
                break

            if self.current_char() == '*' and self.peek_char() == '>':
                comment = self.read_comment()
                continue

            if self.current_char().isdigit():
                self.tokens.append(self.read_number())
                continue

            if self.current_char().isalpha():
                self.tokens.append(self.read_name())
                continue

            start_line = self.line
            start_column = self.column
            char = self.current_char()

            if char == '{':
                self.tokens.append(Token(TokenType.LBRACE, char, start_line, start_column))
                self.advance()
            elif char == '}':
                self.tokens.append(Token(TokenType.RBRACE, char, start_line, start_column))
                self.advance()
            elif char == '[':
                self.tokens.append(Token(TokenType.LBRACKET, char, start_line, start_column))
                self.advance()
            elif char == ']':
                self.tokens.append(Token(TokenType.RBRACKET, char, start_line, start_column))
                self.advance()
            elif char == '(':
                self.tokens.append(Token(TokenType.LPAREN, char, start_line, start_column))
                self.advance()
            elif char == ')':
                self.tokens.append(Token(TokenType.RPAREN, char, start_line, start_column))
                self.advance()
            elif char == ',':
                self.tokens.append(Token(TokenType.COMMA, char, start_line, start_column))
                self.advance()
            elif char == '=':
                self.advance()
                if self.current_char() == '>':
                    self.tokens.append(Token(TokenType.ARROW, '=>', start_line, start_column))
                    self.advance()
                else:
                    self.tokens.append(Token(TokenType.EQUAL, '=', start_line, start_column))
            elif char == '#':
                self.tokens.append(Token(TokenType.HASH, char, start_line, start_column))
                self.advance()
            else:
                raise LexerError(f"Неожиданный символ '{char}'", self.line, self.column)

        self.tokens.append(Token(TokenType.EOF, None, self.line, self.column))
        return self.tokens
