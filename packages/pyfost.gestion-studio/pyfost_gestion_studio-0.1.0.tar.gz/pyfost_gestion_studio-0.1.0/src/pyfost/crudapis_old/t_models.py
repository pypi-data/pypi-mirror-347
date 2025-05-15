# models.py
from tortoise import fields, models


class User(models.Model):
    """
    User model
    """

    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=50, unique=True, index=True)
    email = fields.CharField(max_length=100, unique=True)
    full_name = fields.CharField(max_length=100, null=True)
    active = fields.BooleanField(default=True)

    # Relationship: One user has many posts
    # 'models.Post' uses string to avoid circular import issues
    # 'related_name="author"' links back from the Post model's ForeignKeyField
    posts: fields.ReverseRelation["models.Post"]

    class PydanticMeta:
        # Exclude posts from default Pydantic model for User creation/update via API/Admin
        # Relationships are often handled separately or via IDs.
        exclude = ("posts",)

    def __str__(self) -> str:
        return self.username


class Post(models.Model):
    """
    Post model
    """

    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=200, index=True)
    content = fields.TextField()
    published = fields.BooleanField(default=False)

    # Relationship: Many posts belong to one user
    # Use 'models.User' as string type hint
    # related_name must match the ReverseRelation name in User ('posts')
    author: fields.ForeignKeyRelation["models.User"] = fields.ForeignKeyField(
        "models.User", related_name="posts"
    )

    def __str__(self) -> str:
        return self.title
