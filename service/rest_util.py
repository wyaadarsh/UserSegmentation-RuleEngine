from service.evaluator import Evaluation
from service.validator import ValidateRule
from utils.db_utils import SegmentModel, UserModel


def evaluate_user_segment(user_id, segment_name):
    return Evaluation(
        UserModel().get_user_object(user_id),
        SegmentModel().get_segment_rule(segment_name=segment_name)
    )


def bulk_identify_segment(user_id, segment_list):
    return [segment_name for segment_name in segment_list if evaluate_user_segment(user_id, segment_name)]


def insert_new_segment(segment_details):
    SegmentModel().insert(segment_details)


def insert_new_user(user_details):
    UserModel().insert(user_details)


def bulk_insert_users(user_list):
    UserModel().insert_bulk(user_list)


def bulk_insert_segments(segment_list):
    UserModel().insert_bulk(segment_list)
