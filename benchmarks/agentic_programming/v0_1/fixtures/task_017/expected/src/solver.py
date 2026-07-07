import ast
import operator

def evaluate_expression(expr):
    """Evaluate a mathematical expression and return the numeric result.
    Supports +, -, *, / and parentheses.
    """
    allowed_ops = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.USub: operator.neg,
    }

    def eval_node(node):
        if isinstance(node, ast.Expression):
            return eval_node(node.body)
        elif isinstance(node, ast.Constant):
            if isinstance(node.value, (int, float)):
                return node.value
            raise ValueError("unsupported constant")
        elif isinstance(node, ast.UnaryOp):
            if type(node.op) in allowed_ops:
                return allowed_ops[type(node.op)](eval_node(node.operand))
            raise ValueError("unsupported operator")
        elif isinstance(node, ast.BinOp):
            if type(node.op) in allowed_ops:
                return allowed_ops[type(node.op)](eval_node(node.left), eval_node(node.right))
            raise ValueError("unsupported operator")
        else:
            raise ValueError("unsupported expression")

    tree = ast.parse(expr, mode="eval")
    return eval_node(tree.body)
