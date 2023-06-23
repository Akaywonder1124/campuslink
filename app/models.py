from datetime import datetime
from tortoise.models import Model
from tortoise import fields
from tortoise.contrib.pydantic import pydantic_model_creator

class School(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=100, null=False)
    school_email = fields.CharField(max_length=50, unique=True, null=False)
    school_domain = fields.CharField(max_length=50, unique= True, null = False)
    country = fields.CharField(max_length=50, null=True)

    class Meta:
        table = "school"

class User(Model):
    id = fields.IntField(pk=True)
    full_name = fields.CharField(max_length=100, null=False)
    username = fields.CharField(max_length=30, unique=True, null= False)
    email = fields.CharField(max_length=50, unique=True, null=False)
    about = fields.TextField(default = "about me", null = True)
    profile_pic = fields.CharField(max_length=100, defualt="default.jpg", null=True)
    date_of_birth = fields.DatetimeField(auto_now=True)
    school = fields.ForeignKeyField("models.School", related_name="user_school")
    hashed_password = fields.CharField(max_length=128, null=False)
    member_since = fields.DatetimeField(auto_now_add=True)
    restricted = fields.BooleanField(default=False)
    is_verified = fields.BooleanField(default=False)
    role = fields.ManyToManyField("models.Role", related_name="user", through="user_role")
    event = fields.ManyToManyField("models.Event", related_name="user", through="user_event")
    interest = fields.ManyToManyField("models.Interest", related_name="user", through="user_interest")
    friends = fields.ManyToManyField("models.User", related_name="frieds_with")

    class Meta:
        table = "user"

class Role(Model):
    id = fields.IntField(pk=True)
    role = fields.CharField(max_length=30, null=False)

    class Meta:
        table = "role"

class Interest(Model):
    id = fields.IntField(pk=True, index=True)
    interest_name = fields.CharField(max_length=100, unique=True, null=False)
    description = fields.TextField()
    interest_admin = fields.ForeignKeyField("models.User", related_name="category", null=True)

    class Meta:
        table = "interest"

class Event(Model):
    id = fields.IntField(pk=True, index=True)
    event_name = fields.CharField(max_length=100, null=False)
    event_status = fields.CharField(max_length=50, default="Upcoming")
    event_stus = fields.CharField(max_length=50, default="Upcoming")
    description = fields.TextField()
    venue = fields.TextField(null=False, default="Unknown")
    event_date = fields.DatetimeField(null=False)
    is_appproved = fields.BooleanField(default=False)
    event_category = fields.ForeignKeyField("models.Interest", related_name="event")
    event_creator = fields.ForeignKeyField("models.User", related_name="user_events")
    

    class Meta:
        table = "event"

