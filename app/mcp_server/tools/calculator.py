import ast
import operator


class CalculatorTool:

    OPERATORS = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Mod: operator.mod,
        ast.Pow: operator.pow,
        ast.USub: operator.neg,
    }

    def calculate(
        self,
        expression: str,
    ) -> float:

        expression_ast = ast.parse(
            expression,
            mode="eval",
        )

        return self._evaluate(
            expression_ast.body
        )

    def _evaluate(
        self,
        node,
    ):

        if isinstance(
            node,
            ast.Constant,
        ):
            return node.value

        if isinstance(
            node,
            ast.BinOp,
        ):

            left = self._evaluate(
                node.left
            )

            right = self._evaluate(
                node.right
            )

            operator_type = type(
                node.op
            )

            if operator_type not in self.OPERATORS:
                raise ValueError(
                    "Unsupported operator."
                )

            return self.OPERATORS[
                operator_type
            ](
                left,
                right,
            )

        if isinstance(
            node,
            ast.UnaryOp,
        ):

            operand = self._evaluate(
                node.operand
            )

            operator_type = type(
                node.op
            )

            if operator_type not in self.OPERATORS:
                raise ValueError(
                    "Unsupported operator."
                )

            return self.OPERATORS[
                operator_type
            ](
                operand
            )

        raise ValueError(
            "Invalid expression."
        )