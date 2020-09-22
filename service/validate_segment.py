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
    def __init__(self, user_data, segment_id):
        self.user_data = user_data
        self.rule = db.get_rule(segment_id)

    def validate(self):

        def examine_rule(entities):
            if isinstance(entities, dict):
                if len(entities.keys()) != 1: raise Exception("Invalid Rule")
                entity = next(iter(entities))
                entity_val = entities[entity]
                if entity in allowed_rule_params:
                    return validate_user_data(entity, entity_val)
                if entity in allowed_conjunctors:
                    break_on_true, break_on_false = ConjunctorConfig.get(entity).break_on_true_false()
                    res = None
                    for i in entity_val:
                        result = examine_rule(i)
                        if break_on_true and result: return result
                        if break_on_false and not result: return result
                        if res is None: res = result
                        else: res = ConjunctorConfig.get(entity).evaluate(res, result)
                    return res

        def validate_user_data(entity, entity_val):
            return evaluate_expression(
                entity,
                entity_val.get('op'),
                entity_val.get('value'),
                self.user_data
            )

        return examine_rule(self.rule)


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
        "and": [
            {
                "and":
                [
                    {"gender": {"value": "F", "op": "eq"}},
                    {"gender": {"value": "F", "op": "eq"}}
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
