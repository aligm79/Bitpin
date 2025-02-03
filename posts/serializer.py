from rest_framework import serializers
from posts.models import Post, Comment


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        exclude = ["id", "user"]
        extra_kwargs = {
            "user" : {"required": False},
            "created_date": {"required": False}
        }

class PostsSerializer(serializers.ModelSerializer):
    user_comment = serializers.SerializerMethodField()

    def get_user_comment(self, obj):
         if hasattr(obj, "user_comment") and obj.user_comment:
             return CommentSerializer(obj.user_comment, many=True).data[0]["point"]
         return None

    class Meta:
        model = Post
        exclude = ["body"]