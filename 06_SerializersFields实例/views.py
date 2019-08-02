from .models import User, Topic, Post
from .serializer import UserSerializer, TopicSerializer, PostSerializer
from rest_framework.viewsets import ModelViewSet


class UserViewSet(ModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer


class TopicViewSet(ModelViewSet):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
