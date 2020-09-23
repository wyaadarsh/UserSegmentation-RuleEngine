from service.validator import *
from settings import *
from pymongo import MongoClient

from utils.exceptions import InvalidRuleException, IDNeededException
from utils.singleton_util import SingletonFactory


class MongoAccess(metaclass=SingletonFactory):

    def __init__(self):
        self.client = MongoClient(MONGO_URL)
        self.db = self.client[SEGMENTATION_DB]


class SegmentModel:

    def __init__(self):
        self.client = MongoAccess()
        self.segment_table = self.client.db[SEGMENTS_TABLE]

    def insert(self, json_object):
        segment_rule = json_object.get('segment_rule')
        if not ValidateRule(segment_rule):
            raise InvalidRuleException
        resp = self.segment_table.insert(json_object)

    def insert_bulk(self, json_objects):
        is_valid = all([ValidateRule(segment_rule) for segment_rule in json_objects])
        if not is_valid:
            raise InvalidRuleException
        self.segment_table.insert_many(json_objects)

    def get_segment_rule(self, segment_name):
        res = self.segment_table.find({"segment_name": segment_name})
        for r in res:
            return r.get('segment_rule')


class UserModel:

    def __init__(self):
        self.client = MongoAccess()
        self.user_table = self.client.db[USERS_TABLE]

    def insert(self, json_object):
        if "_id" not in json_object:
            raise IDNeededException
        resp = self.user_table.insert(json_object)

    def insert_bulk(self, json_objects):
        is_valid = all(["_id" in json_object for json_object in json_objects])
        if not is_valid:
            raise IDNeededException
        resp = self.user_table.insert_many(json_objects)

    def get_user_object(self, user_id):
        res = self.user_table.find({"_id": user_id})
        return res


if __name__ == "__main__":
    js = {"test": 1, "test2": 2}
    MongoAccess().rule_table.insert(js)


# - db : repository, entity
# - model: resource
# - service:
