from abc import ABCMeta, abstractmethod


class Conjunctor(metaclass=ABCMeta):

    def __init__(self):
        pass

    @abstractmethod
    def evaluate(self, *kwargs):
        # ret: expression
        pass

    @abstractmethod
    def break_on_true_false(self):
        # break_on_true, break_on_false
        pass


class And_(Conjunctor):

    def _evaluate(self, *kwargs):
        if len(kwargs) < 2:
            return True
        if kwargs[0] == False:
            return False
        if len(kwargs) == 2:
            return kwargs[0] and kwargs[1]
        return kwargs[0] and kwargs[1] and self._evaluate(*kwargs[2:])

    def evaluate(self, *kwargs):
        ret = self._evaluate(*kwargs)
        return ret

    def break_on_true_false(self):
        return False, True


class Or_(Conjunctor):

    def _evaluate(self, *kwargs):
        if len(kwargs) < 2:
            return True
        if kwargs[0] == True:
            return True
        if len(kwargs) == 2:
            return kwargs[0] or kwargs[1]
        return kwargs[0] or kwargs[1] or self._evaluate(*kwargs[2:])

    def evaluate(self, *kwargs):
        ret = self._evaluate(*kwargs)
        return ret

    def break_on_true_false(self):
        return True, False


ConjunctorConfig = {
    "and": And_(),
    "or": Or_(),
}
