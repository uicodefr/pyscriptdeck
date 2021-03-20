import random
from pyscriptdeck.common import ScriptDeck, ScriptDescription, ScriptResult


class CalculatePi(ScriptDeck):
    def __init__(self):
        super().__init__(__name__)

    def get_description(self):
        return ScriptDescription(
            group="demo", name="Calculate Pi",
            description="Estimate Pi with the Monte Carlo method",
            params=[{
                "id": "iterations",
                "type": "number",
                "label": "Number of iterations",
                "default": 50
            }]
        )

    def run(self, data_input):
        max_iteration = self.get_config("maxIteration")
        iterations = int(data_input["iterations"])

        if iterations <= 0:
            return ScriptResult(success=False, message="Number of iterations should be positive")
        if iterations > max_iteration:
            message = "The maximum number of iterations allowed is {}".format(max_iteration)
            return ScriptResult(success=False, message=message)

        points_inside = 0
        for _ in range(iterations):
            x = random.random()
            y = random.random()
            if x**2 + y**2 < 1:
                points_inside += 1

        pi = 4 * points_inside / iterations
        message = "Estimate Pi as {} with {} iterations".format(pi, iterations)
        data = {"iterations": iterations, "pointsInside": points_inside, "pi": pi}
        return ScriptResult(success=True, message=message, dataOutput=data)


class CalculateFibonacci(ScriptDeck):
    def __init__(self):
        super().__init__(__name__)

    def get_description(self):
        return ScriptDescription(
            group="demo", name="Calculate Fibonacci numbers",
            description="Calculate a Fibonacci number at a position",
            params=[{
                "id": "position",
                "type": "number",
                "label": "Position in the Fibonacci sequence",
                "default": 10
            }]
        )

    def run(self, data_input):
        max_position = self.get_config("maxPosition")
        position = int(data_input["position"])

        if position < 0:
            return ScriptResult(success=False, message="Position should be positive")
        if position > max_position:
            message = "The maximum position allowed is {}".format(max_position)
            return ScriptResult(success=False, message=message)

        value = fibonacci(position)
        message = "The fibonacci number at the position {} has the value {}".format(position, value)
        data = {"position": position, "value": value}
        return ScriptResult(success=True, message=message, dataOutput=data)

def fibonacci(position):
    if position < 2:
        return position
    return fibonacci(position-1) + position
