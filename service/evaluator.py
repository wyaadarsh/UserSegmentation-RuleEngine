from utils.exceptions import InvalidRuleException
from utils.operators import operators_config
from utils.conjunctor_config import ConjunctorConfig
from utils.user_getter import UserGetter
from utils.db_utils import MongoAccess
from utils.yaml_util import YAMLReader

import os
cur_dir = os.path.dirname(os.path.realpath(__file__))

db = MongoAccess()

allowed_conjunctors = set(ConjunctorConfig)
allowed_operators = set(operators_config)
allowed_rule_params = set(YAMLReader.load_config_from_yml(cur_dir, "/allowed_rule_params.yaml"))


class Evaluation:
    def __init__(self, user_data, segment_rule):
        self.user_data = user_data
        self.rule = segment_rule

    def validate(self, evaluate=True):

        def examine_rule(entities, evaluate=True):
            if isinstance(entities, dict):
                if len(entities.keys()) != 1: raise InvalidRuleException
                entity = next(iter(entities))
                entity_val = entities[entity]
                if entity in allowed_rule_params:
                    if evaluate: return evaluate_user_data(entity, entity_val)
                    return validate_leaf_level_expression(entity_val)
                if entity in allowed_conjunctors:
                    break_on_true, break_on_false = ConjunctorConfig.get(entity).break_on_true_false()
                    res = None
                    for i in entity_val:
                        result = examine_rule(i, evaluate)
                        if break_on_true and result: return result
                        if break_on_false and not result: return result
                        if res is None: res = result
                        else: res = ConjunctorConfig.get(entity).evaluate(res, result)
                    return res
            raise InvalidRuleException

        def evaluate_user_data(entity, entity_val):
            return evaluate_expression(
                entity,
                entity_val.get('op'),
                entity_val.get('value'),
                self.user_data
            )

        def validate_leaf_level_expression(entity_val):
            return expression_validator(
                entity_val.get('op'),
                entity_val.get('value')
            )

        return examine_rule(self.rule, evaluate)


def expression_validator(operator, value):
    if operator not in allowed_operators:
        raise InvalidRuleException
    return True

def evaluate_expression(entity, operator, value, user_data):
    val = UserGetter(user_data).get_entity(entity)
    if val:
        try:
            if operators_config.get(operator)(val, value): return True
        except Exception as e:
            print("Exception {} while evaluating {}".format(e, entity))
    return False


if __name__ == "__main__":
    segment_1 = {
        "or": [
            {
                "or":
                [
                    {"gender": {"value": "F", "op": "eq"}},
                    {"gender": {"value": "M", "op": "eq"}}
                ]
            },
            {
                "or":
                    [
                        {
                            "and": [
                                {"gender": {"value": "F", "op": "eq"}},
                                {"gender": {"value": "F", "op": "eq"}}
                            ]
                        },
                        {
                            "age": {"value": "15", "op": "eq"}
                        }
                    ]
            }
        ]
    }

    # Leaf level dict
    # list of evaluatable entitites superceeded by operator


    user_data = {
        "name": "Asha",
        "gender": "F",
        "age": 15
    }
    print(Evaluation(user_data, 1).validate())

    user_data = {
        "name": "Asha1",
        "gender": "M",
        "age": 20
    }
    print(Evaluation(user_data, 1).validate())