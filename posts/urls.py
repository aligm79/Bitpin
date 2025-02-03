from django.urls import path
from posts import views


urlpatterns = [
    path("list/", views.PostsListAPIView.as_view(), name="list"),
    path("create/comment/", views.CommentCreateAPIView.as_view(), name="comment")
]