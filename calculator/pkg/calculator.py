# calculator.py
import re

class Calculator:
    def evaluate(self, expression):
        if not expression:
            return None

        # Basic regex to find numbers and operators
        tokens = re.findall(r'\d+|\S', expression)

        # Simple RPN-like evaluation for demonstration
        # This is a highly simplified evaluator and not production-ready
        output_queue = []
        operator_stack = []
        
        precedence = {'+': 1, '-': 1, '*': 2, '/': 2}

        for token in tokens:
            if token.isdigit():
                output_queue.append(float(token))
            elif token in '+-*/':
                while (operator_stack and 
                       operator_stack[-1] in precedence and 
                       precedence[operator_stack[-1]] >= precedence[token]):
                    output_queue.append(operator_stack.pop())
                operator_stack.append(token)
            else:
                raise ValueError(f"Invalid token: {token}")

        while operator_stack:
            output_queue.append(operator_stack.pop())

        # Evaluate RPN
        eval_stack = []
        for token in output_queue:
            if isinstance(token, float):
                eval_stack.append(token)
            else:
                # Token is an operator
                if len(eval_stack) < 2:
                    raise ValueError("Not enough operands for operator")
                b = eval_stack.pop()
                a = eval_stack.pop()
                if token == '+':
                    eval_stack.append(a + b)
                elif token == '-':
                    eval_stack.append(a - b)
                elif token == '*':
                    eval_stack.append(a * b)
                elif token == '/':
                    if b == 0:
                        raise ValueError("Division by zero")
                    eval_stack.append(a / b)
        
        if len(eval_stack) != 1:
            raise ValueError("Invalid expression")
        
        # Return as integer if it's a whole number, otherwise float
        result = eval_stack[0]
        if result == int(result):
            return int(result)
        return result