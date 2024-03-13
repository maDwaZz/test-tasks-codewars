# Simpler Interactive Interpreter
# https://www.codewars.com/kata/53005a7b26d12be55c000243/train/python

import re


class VariableNotPresentException(ValueError):
    pass


def tokenize(expression):
    if expression == "":
        return []

    regex = re.compile("\s*(=>|[-+*\/\%=\(\)]|[A-Za-z_][A-Za-z0-9_]*|[0-9]*\.?[0-9]+)\s*")
    tokens = regex.findall(expression)
    return [s for s in tokens if not s.isspace()]


class Interpreter:
    OPERATORS = {
        "*": (2, lambda x, y: x * y),  # 2 - более высокий приоритет оператора
        "/": (2, lambda x, y: x / y),
        "%": (2, lambda x, y: x % y),
        "+": (1, lambda x, y: x + y),
        "-": (1, lambda x, y: x - y)
    }

    def __init__(self):
        self.vars = {}
        self.functions = {}

    def input(self, expression):
        if expression.strip() == "":
            return ""

        tokens = tokenize(expression)

        if len(tokens) > 1 and tokens[1] == "=" and re.match(r"[A-Za-z_][A-Za-z0-9_]*", tokens[0]):
            self.vars[tokens[0]] = self.calc(tokens[2:])
            return self.vars[tokens[0]]

        else:
            return self.calc(tokens)

    def shunting_yard(self, tokens):
        """
        Алгоритм сортировочной станции - генератор, получает на вход итерируемый объект из чисел и операторов
        в инфиксной нотации, возвращает числа и операторов в обратной польской записи.
        """
        stack = []

        for token in tokens:
            if token in self.OPERATORS:
                while stack and stack[-1] != "(" and self.OPERATORS[token][0] <= self.OPERATORS[stack[-1]][0]:
                    yield stack.pop()
                stack.append(token)

            elif token == ")":
                while stack:
                    x = stack.pop()
                    if x == "(":
                        break
                    yield x

            elif token == "(":
                stack.append(token)

            else:
                yield token if token not in self.vars else self.vars[token]

        while stack:
            yield stack.pop()

    def calc(self, tokens):
        if not tokens:
            return

        if len(tokens) > 1 and all(token not in self.OPERATORS for token in tokens):
            raise ValueError

        for token in tokens:
            if re.match(r"[A-Za-z_][A-Za-z0-9_]*", token) and token not in self.vars:
                raise VariableNotPresentException(f"Invalid identifier. No variable with name '{token}' was found.")

        polish_notation_tokens = self.shunting_yard(tokens)
        stack = []

        for token in polish_notation_tokens:
            if token in self.OPERATORS:
                y, x = stack.pop(), stack.pop()
                stack.append(self.OPERATORS[token][1](float(x), float(y)))

            else:
                stack.append(float(token))

        return stack[0]
