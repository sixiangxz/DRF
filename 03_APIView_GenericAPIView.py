# model----------------------------------------------------------------------------
from django.db import models
class Post(models.Model):

    title = models.CharField(max_length=100)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ("created",)

# serializer------------------------------------------------------------------------
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

# view------------------------------------------------------------------------------
from app1.models import Post
from app1.serializers import PostSerializer, AdminSerializer
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import mixins
class PostList(generics.ListCreateAPIView):

    queryset = Post.objects.all()
    serializer_class = PostSerializer


class DetailPost(mixins.RetrieveModelMixin,
                 mixins.UpdateModelMixin,
                 mixins.DestroyModelMixin,
                 generics.GenericAPIView):

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    # 把path改为path('posts/<int:sn>', views.DetailPost.as_view(), name='post-detail')
    # 否则在get_object(self)会出现断言错误 assert lookup_url_kwarg in self.kwargs
    lookup_url_kwarg = "sn"
    # 默认是pk，修改之后会利用title查找模型（如.../posts/your_title/）完全匹配如果title，如果不唯一，则可能出现多值
    # 把path改为path('posts/<str:sn>', views.DetailPost.as_view(), name='post-detail')
    # filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]} 如{'pk':"1"}
    # obj = get_object_or_404(queryset, **filter_kwargs)    查找
    lookup_field = 'title'

    # 需要重写get方法，返回retrieve(),否则访问127.0.0.1:8000/posts/1/时会显示找不到GET方法
    def get(self, request, *args, **kwargs):

        return self.retrieve(self,request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    # 仅仅显示get
    # def list(self, request, *args, **kwargs):
    #
    #     queryset = self.get_queryset()
    #     serializer = PostSerializer(queryset, many=True)
    #     return Response(serializer.data)
    # 通过指定get_serializer_class的返回，来确定使用那个序列化类
    # def get_serializer_class(self):
    #
    #     if self.request.user.is_staff:
    #         return AdminSerializer
    #     return PostSerializer

# url------------------------------------------------------------------------------
from django.urls import path
from app1 import views

urlpatterns = [
    path('posts/', views.PostList.as_view(), name='post-list'),
    path('posts/<int:sn>', views.DetailPost.as_view(), name='post-detail')

]