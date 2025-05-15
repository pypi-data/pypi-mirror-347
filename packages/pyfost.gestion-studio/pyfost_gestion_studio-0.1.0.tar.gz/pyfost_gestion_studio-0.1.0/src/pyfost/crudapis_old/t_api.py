from tortoise_api.api import Model, Api
from tortoise import fields


class User(Model):
    id: int = fields.IntField(pk=True)
    name: str = fields.CharField(255, unique=True, null=False)
    posts: fields.ReverseRelation["Post"]


class Post(Model):
    id: int = fields.IntField(pk=True)
    text: str = fields.CharField(4095)
    user: User = fields.ForeignKeyField("models.User", related_name="posts")
    _name = "text"  # `_name` sets the attr for displaying related Post instace inside User (default='name')

import t_models

api = Api(t_models, "sqlite://./db_tortoise_fallback.sqlite3", "MY_SUPER_SECRET_tortoise"), AuthRouter, True, "Pswd Example")
api.gen_routes()