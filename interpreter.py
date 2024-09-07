class Environment:
    def __init__(self):
        self.variables = {}

    def get(self, name):
        return self.variables.get(name)

    def set(self, name, value):
        self.variables[name] = value

class Interpreter:
    def __init__(self):
        self.env = Environment()

    def visit(self, node):
        method_name = f'visit_{type(node).__name__}'
        method = getattr(self, method_name, self.generic_visit)
        return method(node)

    def generic_visit(self, node):
        raise Exception(f'No visit_{type(node).__name__} method')

    def visit_NumberNode(self, node):
        return node.value

    def visit_BinOpNode(self, node):
        if node.op == 'PLUS':
            return self.visit(node.left) + self.visit(node.right)
        elif node.op == 'MINUS':
            return self.visit(node.left) - self.visit(node.right)
        elif node.op == 'MULTIPLY':
            return self.visit(node.left) * self.visit(node.right)
        elif node.op == 'DIVIDE':
            return self.visit(node.left) / self.visit(node.right)

    def visit_VarAssignNode(self, node):
        value = self.visit(node.value)
        self.env.set(node.name, value)
        return value

    def visit_VarAccessNode(self, node):
        value = self.env.get(node.name)
        if value is None:
            raise Exception(f"Undefined variable '{node.name}'")
        return value

    def visit_FuncDefNode(self, node):
        self.env.set(node.name, node)
        return node

    def visit_FuncCallNode(self, node):
        func = self.env.get(node.name)
        if not func:
            raise Exception(f"Undefined function '{node.name}'")
        # Handle function calls, argument passing, etc.
        pass

    def visit_IfNode(self, node):
        condition = self.visit(node.condition)
        if condition:
            return self.visit(node.true_body)
        elif node.false_body:
            return self.visit(node.false_body)

# Example of running the interpreter
def main():
    source_code = '''
    func add(a, b) {
        return a + b;
    }
    print(add(3, 4));
    '''
    lexer = Lexer(source_code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    interpreter = Interpreter()
    for statement in ast:
        interpreter.visit(statement)

if __name__ == "__main__":
    main()
