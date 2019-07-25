from snippets.models import Snippet
from snippets.serializers import SnippetSerializer
from rest_framework import generics
from snippets.serializers import UserSerializer
from django.contrib.auth.models import User
from rest_framework import permissions
from snippets.permissions import IsOwnerOrReadOnly
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import renderers
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
class SnippetViewSet(viewsets.ModelViewSet):

    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)

    @action(detail=True, renderer_classes=[renderers.StaticHTMLRenderer])
    def highlight(self, request, *args,**kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    # 1.写一个list方法(通过get访问时会调用此方法)，覆盖ModelViewSet继承mixins.ListModelMixin里面的list,
    def list(self, request, *args, **kwargs):
        # 父类中的list方法
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        res = Response(serializer.data)
        print(res.data)  # [OrderDict([('url','...')])]
        print(res.status_code)  # 200
        print(res.status_text)  # OK
        print(res.template_name)  # None
        return res

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """ 这个视图集会自动提供`list`和 `detail`操作 """
    queryset = User.objects.all()
    serializer_class = UserSerializer