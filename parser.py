class ASTNode:
    pass

class NumberNode(ASTNode):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f'NumberNode({self.value})'

class BinOpNode(ASTNode):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

    def __repr__(self):
        return f'BinOpNode({self.left}, {self.op}, {self.right})'

class VarAssignNode(ASTNode):
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __repr__(self):
        return f'VarAssignNode({self.name}, {self.value})'

class VarAccessNode(ASTNode):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f'VarAccessNode({self.name})'

class FuncDefNode(ASTNode):
    def __init__(self, name, params, body):
        self.name = name
        self.params = params
        self.body = body

    def __repr__(self):
        return f'FuncDefNode({self.name}, {self.params}, {self.body})'

class FuncCallNode(ASTNode):
    def __init__(self, name, args):
        self.name = name
        self.args = args

    def __repr__(self):
        return f'FuncCallNode({self.name}, {self.args})'

class IfNode(ASTNode):
    def __init__(self, condition, true_body, false_body):
        self.condition = condition
        self.true_body = true_body
        self.false_body = false_body

    def __repr__(self):
        return f'IfNode({self.condition}, {self.true_body}, {self.false_body})'

class WhileNode(ASTNode):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

    def __repr__(self):
        return f'WhileNode({self.condition}, {self.body})'

class ReturnNode(ASTNode):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f'ReturnNode({self.value})'

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.current_token = self.tokens[self.pos]

    def advance(self):
        self.pos += 1
        self.current_token = self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def eat(self, token_type):
        if self.current_token and self.current_token.type == token_type:
            self.advance()
        else:
            raise Exception(f"Unexpected token: {self.current_token}, expected: {token_type}")

    def parse(self):
        statements = []
        while self.current_token is not None:
            if self.current_token.type == 'KEYWORD' and self.current_token.value == 'func':
                statements.append(self.func_def())
            elif self.current_token.type == 'KEYWORD' and self.current_token.value == 'if':
                statements.append(self.if_statement())
            elif self.current_token.type == 'KEYWORD' and self.current_token.value == 'while':
                statements.append(self.while_statement())
            elif self.current_token.type == 'KEYWORD' and self.current_token.value == 'return':
                statements.append(self.return_statement())
            else:
                statements.append(self.expr())
        return statements

    def func_def(self):
        self.eat('KEYWORD')  # 'func'
        func_name = self.current_token.value
        self.eat('IDENTIFIER')
        self.eat('LPAREN')
        params = []
        while self.current_token.type != 'RPAREN':
            params.append(self.current_token.value)
            self.eat('IDENTIFIER')
            if self.current_token.type == 'COMMA':
                self.eat('COMMA')
        self.eat('RPAREN')
        self.eat('LCURLY')
        body = []
        while self.current_token and self.current_token.type != 'RCURLY':
            body.append(self.expr())
        self.eat('RCURLY')
        return FuncDefNode(func_name, params, body)

    def if_statement(self):
        self.eat('KEYWORD')  # 'if'
        self.eat('LPAREN')
        condition = self.expr()
        self.eat('RPAREN')
        self.eat('LCURLY')
        true_body = []
        while self.current_token and self.current_token.type != 'RCURLY':
            true_body.append(self.expr())
        self.eat('RCURLY')

        false_body = None
        if self.current_token and self.current_token.type == 'KEYWORD' and self.current_token.value == 'else':
            self.eat('KEYWORD')  # 'else'
            self.eat('LCURLY')
            false_body = []
            while self.current_token and self.current_token.type != 'RCURLY':
                false_body.append(self.expr())
            self.eat('RCURLY')

        return IfNode(condition, true_body, false_body)

    def while_statement(self):
        self.eat('KEYWORD')  # 'while'
        self.eat('LPAREN')
        condition = self.expr()
        self.eat('RPAREN')
        self.eat('LCURLY')
        body = []
        while self.current_token and self.current_token.type != 'RCURLY':
            body.append(self.expr())
        self.eat('RCURLY')
        return WhileNode(condition, body)

    def return_statement(self):
        self.eat('KEYWORD')  # 'return'
        value = self.expr()
        return ReturnNode(value)

    def expr(self):
        node = self.term()

        while self.current_token and self.current_token.type in ('PLUS', 'MINUS'):
            op = self.current_token.type
            self.eat(op)
            node = BinOpNode(node, op, self.term())

        return node

    def term(self):
        node = self.factor()

        while self.current_token and self.current_token.type in ('MULTIPLY', 'DIVIDE'):
            op = self.current_token.type
            self.eat(op)
            node = BinOpNode(node, op, self.factor())

        return node

    def factor(self):
        token = self.current_token

        if token.type == 'NUMBER':
            self.eat('NUMBER')
            return NumberNode(token.value)

        elif token.type == 'IDENTIFIER':
            self.eat('IDENTIFIER')
            if self.current_token and self.current_token.type == 'LPAREN':
                return self.func_call(token.value)
            return VarAccessNode(token.value)

        elif token.type == 'LPAREN':
            self.eat('LPAREN')
            node = self.expr()
            self.eat('RPAREN')
            return node

        elif token.type == 'KEYWORD' and token.value == 'return':
            return self.return_statement()

        raise Exception(f"Unexpected token: {token}")

    def func_call(self, func_name):
        self.eat('LPAREN')
        args = []
        while self.current_token and self.current_token.type != 'RPAREN':
            args.append(self.expr())
            if self.current_token and self.current_token.type == 'COMMA':
                self.eat('COMMA')
        self.eat('RPAREN')
        return FuncCallNode(func_name, args)
