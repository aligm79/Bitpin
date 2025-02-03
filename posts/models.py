from django.db import models
import uuid
from django.contrib.auth.models import User
from datetime import datetime

class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=20, blank=False, null=False)
    body = models.CharField(max_length=200, blank=False, null=False)
    avg_point = models.FloatField(default=0)
    number_of_people = models.IntegerField(default=0)

class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    point = models.IntegerField()
    created_date = models.DateTimeField(null=False, blank=False)
    is_dirty = models.BooleanField(default=False)
    
    class Meta:
        indexes = [
            models.Index(fields=["user", "post"]),
            models.Index(fields=["created_date"])
        ]
        constraints = [
            models.CheckConstraint(
                check=models.Q(point__gte=0, point__lte=5),
                name="point_between_0_to_5"
            ),
        ]