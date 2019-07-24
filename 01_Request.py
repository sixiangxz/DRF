from snippets.models import Snippet
from snippets.serializers import SnippetSerializer
from snippets.serializers import UserSerializer
from django.contrib.auth.models import User
from rest_framework import permissions
from snippets.permissions import IsOwnerOrReadOnly
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
    # 目的是为了通过访问snippets的url时添加一些自己想查看的内容
    def list(self, request, *args, **kwargs):
        print('request.data......', request.data)
        print('request.query_params......', request.query_params)
        print('request.parsers......', request.parsers)
        print('request.authenticators......', request.authenticators)
        print('request.user......', request.user)
        print('request.auth......', request.auth)
        # 父类super中的list要返回一个Response实例，因此需要通过return接受list的返回值
        # 这里返回的是None， 因此返回父类中的返回值就行
        return super(SnippetViewSet, self).list(request, *args, **kwargs)
    # 此方法处理的是post请求
    def create(self, request, *args, **kwargs):
        print('request.data......', request.data)
        print('request.query_params......', request.query_params)
        print('request.parsers......', request.parsers)
        print('request.authenticators......', request.authenticators)
        print('request.user......', request.user)
        print('request.auth......', request.auth)
        return super(SnippetViewSet, self).create(request, *args, **kwargs)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """ 这个视图集会自动提供`list`和 `detail`操作 """
    queryset = User.objects.all()
    serializer_class = UserSerializer
# 用postman向后台发送数据
# 1.1用get访问snippets: "http://127.0.0.1:8000/snippets"  结果如下：
# request.data...... {}
# request.query_params...... <QueryDict: {}>
# request.parsers...... [<rest_framework.parsers.JSONParser object at 0x000002252BFDF0F0>, <rest_framework.parsers.FormParser object at 0x000002252BFDF0B8>, <rest_framework.parsers.MultiPartParser object at 0x000002252BD3FDD8>]
# request.authenticators...... [<rest_framework.authentication.SessionAuthentication object at 0x000002252BD3FC88>, <rest_framework.authentication.BasicAuthentication object at 0x000002252BD3FFD0>]
# request.user...... jack
# request.auth...... None

# 1.2在body中添加 {
#     "code":"print('hiehei')"
# }再通过get访问snippet   "http://127.0.0.1:8000/snippets?name=tom&age=18"
# 发生变化的结果如下
# request.data...... {'code': "print('hiehei')"}
# request.query_params...... <QueryDict: {'name': ['tom'], 'age': ['18']}>
# request.user...... AnonymousUser
"""
request.data                 发送时body里面的内容
显示AnonymousUser             因为在postman发送时没有提供登录信息
request.query_params         就是Django原生的request.GET


在python中通过property装饰器如：
@property
    def aaa(self):
调用时可通过xxx.aaa
"""
# 2.用post在body中添加 {
#      "code":"print('this is a code')"
#  }方法访问snippets: "http://127.0.0.1:8000/snippets"时
# 需要提供认证，我选择Basic Auth，输入用户名和密码.
# 发生变化的结果如下
# request.data...... {'code': "print('this is a code')"}
# request.query_params...... <QueryDict: {}>
# request.user...... jack
# request.auth...... None
