import re

class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __repr__(self):
        return f'Token({self.type}, {repr(self.value)})'


class Lexer:
    def __init__(self, source_code):
        self.source_code = source_code
        self.tokens = []
        self.current_char = ''
        self.pos = -1
        self.advance()

    def advance(self):
        self.pos += 1
        self.current_char = self.source_code[self.pos] if self.pos < len(self.source_code) else None

    def tokenize(self):
        while self.current_char is not None:
            if self.current_char.isspace():
                self.advance()
            elif self.current_char.isdigit():
                self.tokens.append(self.make_number())
            elif self.current_char.isalpha() or self.current_char == '_':
                self.tokens.append(self.make_identifier())
            elif self.current_char == '"':
                self.tokens.append(self.make_string())
            elif self.current_char in '+-*/()=':
                self.tokens.append(self.make_operator())
            else:
                raise Exception(f"Illegal character '{self.current_char}'")
        return self.tokens

    def make_number(self):
        num_str = ''
        while self.current_char is not None and (self.current_char.isdigit() or self.current_char == '.'):
            num_str += self.current_char
            self.advance()
        return Token('NUMBER', float(num_str) if '.' in num_str else int(num_str))

    def make_identifier(self):
        id_str = ''
        while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '_'):
            id_str += self.current_char
            self.advance()
        if id_str in ['if', 'else', 'while', 'for', 'func', 'return', 'print']:
            return Token('KEYWORD', id_str)
        return Token('IDENTIFIER', id_str)

    def make_string(self):
        string_val = ''
        self.advance()  # Skip the opening quote
        while self.current_char is not None and self.current_char != '"':
            string_val += self.current_char
            self.advance()
        self.advance()  # Skip the closing quote
        return Token('STRING', string_val)

    def make_operator(self):
        op_char = self.current_char
        self.advance()
        if op_char == '=' and self.current_char == '=':
            self.advance()
            return Token('EQ', '==')
        return Token('OPERATOR', op_char)
