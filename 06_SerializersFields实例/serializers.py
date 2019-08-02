from app1.models import Post
from rest_framework.serializers import ModelSerializer
class PostSerializer(ModelSerializer):

    class Meta:
        model = Post
        fields = ('id', 'content', 'title', 'created')


class AdminSerializer(ModelSerializer):

    class Meta:
        model = Post
        fields = ('id', 'content', 'title')
