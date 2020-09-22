import datetime
from mongoengine import Document, StringField, DateTimeField, IntField, EmailField, MapField
import mongoengine


class User(Document):
    user_name = StringField(required=True, max_length=20)
    gender = StringField(required=True, choices=('M', 'F'))
    city = StringField(required=False, max_length=20)
    last_updated = DateTimeField(default=datetime.datetime.now)
    yob = IntField(required=True, max_value=2050, min_value=1920)
    email = EmailField(required=False)
    preference = MapField()

class Rule(Document):
    pass

