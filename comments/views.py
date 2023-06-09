from .models import Comment
from rest_framework.generics import (ListCreateAPIView,
                                     UpdateAPIView,
                                     DestroyAPIView)
from .serializers import CommentSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from posts.models import Post
from users.models import User
from django.shortcuts import get_object_or_404
from .permissions import IsCommentOwner


class CommentsView(ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_queryset(self):
        id_post = self.kwargs['id_post']
        comments = Comment.objects.filter(publication=id_post)
        return comments

    def perform_create(self, serializer):
        id_post = self.kwargs['id_post']
        id_user = self.request.user.id
        post = get_object_or_404(Post, pk=id_post)
        user = get_object_or_404(User, pk=id_user)
        serializer.save(publication=post, user=user)


class CommentsDetailView(UpdateAPIView, DestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsCommentOwner]

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    lookup_url_kwarg = "id_comment"

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    def perform_destroy(self, instance):
        instance.delete()
