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

    def evaluate(self):

        def examine_rule(entities):
            if isinstance(entities, dict):
                if len(entities.keys()) != 1: raise Exception("Invalid Rule")
                entity = next(iter(entities))
                entity_val = entities[entity]
                if entity in allowed_conjunctors:
                    continue_, return_ = evaluate_conjunctor(entity, entity_val)
                    if not continue_: return return_
                return validate_user_data(entity, entity_val)

        def evaluate_conjunctor(entity, entity_val):
            eval_func = ConjunctorConfig.get(entity)
            if not isinstance(entity_val, list):
                raise Exception("Invalid Rule")
            for i in entity_val:
                val, break_on_true, break_on_false = examine_rule(i)
                if val and break_on_true: return False, val
                if not val and break_on_false: return False, val
                return True, val

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
            ["rule0"],
            [
                {
                    "or":
                        [
                            [
                                {"gender": {"value": "F", "op": "eq"}},
                                {"gender": {"value": "F", "op": "eq"}}
                            ],
                            [
                                {"age": {"value": "15", "op": "eq"}}
                            ],
                            [
                                {"and": {"rule4", "rule5"}}
                            ]
                        ]
                }
            ]
        ]
    }
