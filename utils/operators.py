from abc import ABCMeta, abstractmethod


class Operator(metaclass=ABCMeta):

    def __init__(self):
        pass

    @abstractmethod
    def evaluate(self, *kwargs):
        pass


class LessThan(Operator):

    def evaluate(self, *kwargs):
        if len(kwargs) < 2:
            raise Exception("Insufficient Arguments")
        if len(kwargs) == 2:
            return kwargs[0] < kwargs[1]
        return kwargs[0] < kwargs[1] and self.evaluate(*kwargs[1:])


class GreaterThan(Operator):

    def evaluate(self, *kwargs):
        if len(kwargs) < 2:
            raise Exception("Insufficient Arguments")
        if len(kwargs) == 2:
            return kwargs[0] > kwargs[1]
        return kwargs[0] > kwargs[1] and self.evaluate(*kwargs[1:])


class LessThanEqualTo(Operator):

    def evaluate(self, *kwargs):
        if len(kwargs) < 2:
            raise Exception("Insufficient Arguments")
        if len(kwargs) == 2:
            return kwargs[0] <= kwargs[1]
        return kwargs[0] <= kwargs[1] and self.evaluate(*kwargs[1:])


class GreaterThanEqualTo(Operator):

    def evaluate(self, *kwargs):
        if len(kwargs) < 2:
            raise Exception("Insufficient Arguments")
        if len(kwargs) == 2:
            return kwargs[0] >= kwargs[1]
        return kwargs[0] >= kwargs[1] and self.evaluate(*kwargs[1:])


class EqualTo(Operator):

    def evaluate(self, *kwargs):
        if len(kwargs) < 2:
            raise Exception("Insufficient Arguments")
        if len(kwargs) == 2:
            return kwargs[0] == kwargs[1]
        return kwargs[0] == kwargs[1] and self.evaluate(*kwargs[1:])


class NotEqualTo(Operator):

    def evaluate(self, *kwargs):
        if len(kwargs) < 2:
            raise Exception("Insufficient Arguments")
        if len(kwargs) == 2:
            return kwargs[0] != kwargs[1]
        return kwargs[0] > kwargs[1] and self.evaluate(*kwargs[1:])


operators_config = {
    "lt": LessThan().evaluate,
    "lte": LessThanEqualTo().evaluate,
    "gt": GreaterThan().evaluate,
    "gte": GreaterThanEqualTo().evaluate,
    "eq": EqualTo().evaluate,
    "neq": NotEqualTo().evaluate
}

if __name__ == "__main__":
    print(operators_config.get("lt")(3))
