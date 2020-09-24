from mongoengine import Document, StringField, DateTimeField, IntField, EmailField, MapField, DictField, connect
from utils.exceptions import InvalidArgumentException, InvalidRuleException
from service.validator import ValidateRule
from settings import *

connect(db=SEGMENTATION_DB, host=MONGO_URL)


class Segments(Document):
    segment_name = StringField(required=True, max_length=20, primary_key=True)
    segment_rule = DictField(required=True)
    modified_timestamp = DateTimeField()
    modified_by = StringField(max_length=20)


class SegmentModelUtil():

    def __init__(self):
        pass

    def insert(self, json_object):
        segment_name = json_object.get('segment_name')
        segment_rule = json_object.get('segment_rule')
        if not ValidateRule(segment_rule):
            raise InvalidRuleException
        resp = Segments(segment_name=segment_name, segment_rule=segment_rule).save()
        pass

    def insert_bulk(self, json_objects):
        if not isinstance(json_objects, list):
            raise InvalidArgumentException
        update_list = []
        for json_object in json_objects:
            segment_name = json_object.get('segment_name')
            segment_rule = json_object.get('segment_rule')
            if not ValidateRule(segment_rule):
                raise InvalidRuleException
            update_list.append(Segments(segment_name=segment_name, segment_rule=segment_rule))
        Segments.objects.insert(update_list)

    def get_segment_rule(self, segment_name):
        data = Segments.objects(segment_name=segment_name)
        if data:
            return data.segment_rule
        return None


if __name__ == "__main__":
    # segment_1 = {
    #     "or": [
    #         {
    #             "or":
    #                 [
    #                     {"gender": {"value": "F", "op": "eq"}},
    #                     {"gender": {"value": "M", "op": "eq"}}
    #                 ]
    #         },
    #         {
    #             "or":
    #                 [
    #                     {
    #                         "and": [
    #                             {"gender": {"value": "F", "op": "eq"}},
    #                             {"gender": {"value": "F", "op": "eq"}}
    #                         ]
    #                     },
    #                     {
    #                         "age": {"value": "15", "op": "eq"}
    #                     }
    #                 ]
    #         }
    #     ]
    # }
    # segment = {
    #     "segment_name": "segment_1",
    #     "segment_rule": segment_1
    # }

    segment = {
        "segment_name": "segment_11",
        "segment_rule": {
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
    }
    {
        "_id": 10001,
        "gender": "M",
        "name": "John doe",
        "city": "Mumbai",
        "email": "xyz@abc.com",
        "age": 34
    }
    SegmentModelUtil().insert(segment)
    # SegmentModelUtil().get_segment_rule('segment_11')
