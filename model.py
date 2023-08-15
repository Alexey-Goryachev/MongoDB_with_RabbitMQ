from mongoengine import Document
from mongoengine.fields import ListField, StringField, BooleanField

#model for creating a Contacts collection
class Contacts(Document):
    fullname = StringField(max_length=25)
    email = StringField(max_length=35)
    number_phone = StringField(max_length=25)
    address = StringField(max_length=80)
    preferred_method = StringField()
    done = BooleanField(default=False)
    meta = {'allow_inheritance': True}

