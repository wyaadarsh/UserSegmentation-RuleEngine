from service.evaluator import Evaluation


class ValidateRule:

    def __init__(self, rule):
        self.eval_func = Evaluation(None, rule)

    def validate(self):
        return self.eval_func.validate(evaluate=False)
