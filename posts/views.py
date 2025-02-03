import datetime
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from posts.serializer import PostsSerializer, CommentSerializer
from posts.models import Post, Comment
from posts.paginator import CustomPageNumberPagination
from django.core.cache import cache
from django.db.models import Prefetch
from posts.exceptions import PointBetween0And5


class PostsListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PostsSerializer
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        user_comments = Comment.objects.filter(user=self.request.user)
        posts = cache.get("posts")
        if not posts:
            posts = Post.objects.all()
            cache.set("posts", posts, 60)

        return posts.prefetch_related(
            Prefetch("comment_set", queryset=user_comments, to_attr="user_comment")
        )

    def get(self, request, *args, **kwargs):
        qs = self.get_queryset()
        page = self.paginate_queryset(qs)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(data=serializer.data)
    
class CommentCreateAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CommentSerializer

    def post(self, request, *args, **kwargs):
        data = self.request.data
        if data["point"] > 5 or data["point"] < 0:
            raise PointBetween0And5()
        
        comment, _ = Comment.objects.update_or_create(
            user=self.request.user, post_id=data.get("post"),
            defaults={"point": data.get("point"), "created_date": datetime.datetime.now()}
        )
        return Response(self.get_serializer(comment).data, status=status.HTTP_201_CREATED)