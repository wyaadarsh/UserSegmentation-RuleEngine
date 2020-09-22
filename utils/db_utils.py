from settings import *
from pymongo import MongoClient


class SingletonFactory(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(SingletonFactory, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class MongoAccess(metaclass=SingletonFactory):

    def __init__(self):
        self.client = MongoClient(MONGO_URL)
        self.db = self.client[SEGMENTATION_DB]
        if self.db:
            self.users_table = self.db[USERS_TABLE]
            self.rule_table = self.db[RULES_TABLE]

    def get_user(self, user_id):
        pass

    def get_rule(self, rule_id):
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
        return segment_1

    def set_rule(self, rule_name, data):
        pass

    def set_user(self, user_id, user_data):
        pass

# - db : repository, entity
# - model: resource
# - service:
