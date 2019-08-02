from app1.models import Post
from app1.serializers import PostSerializer, AdminSerializer
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import mixins, renderers
class PostList(generics.ListCreateAPIView):

    queryset = Post.objects.all()
    serializer_class = PostSerializer


class DetailPost(mixins.RetrieveModelMixin,
                 mixins.UpdateModelMixin,
                 mixins.DestroyModelMixin,
                 generics.GenericAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get(self, request, *args, **kwargs):

        return self.retrieve(self,request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


from django.shortcuts import get_object_or_404
# 自定义多字段查询
class MultipleFieldLookupMixin(object):

    # 重写部分GenericAPIView里面的get_object方法
    def get_object(self):
        queryset = self.get_queryset()
        queryset = self.filter_queryset(queryset)
        filter = {}
        for field in self.lookup_fields:
            if self.kwargs[field]:
                filter[field] = self.kwargs[field]
        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)

        return obj

class RetrievePostView(MultipleFieldLookupMixin, generics.RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_fields = ('pk', 'title')

from rest_framework import views
from rest_framework import parsers
# class FileUploadView(views.APIView):
#     def post(self, request):
#         print(request.body)
#         return Response('200 ok')
class FileUploadView(views.APIView):
    parser_classes = (parsers.FileUploadParser, )
    def post(self, request, filename, format=None):
        file_obj = request.data['file']
        print(file_obj)
        print(type(file_obj))
        return Response(status=204)
