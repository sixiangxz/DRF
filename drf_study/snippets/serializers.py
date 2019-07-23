from rest_framework import serializers
from snippets.models import Snippet, LANGUAGE_CHOICES, STYLE_CHOICES
from django.contrib.auth.models import User

# class SnippetSerializer(serializers.Serializer):
#     """
#     id ：只读不用管
#     created: 自动创建
#     """
#     id = serializers.ImageField(read_only=True)
#     title = serializers.CharField(required=False, allow_blank=True, max_length=100)
#     code = serializers.CharField(style={'base_template': 'textarea.html'})
#     linenos = serializers.BooleanField(required=False)
#     language = serializers.ChoiceField(choices=LANGUAGE_CHOICES, default='python')
#     style = serializers.ChoiceField(choices=STYLE_CHOICES, default="friendly")
#
#     def create(self, validated_data):
#         # ORM的api创建新片段
#         return Snippet.objects.create(**validated_data)
#
#     def update(self, instance, validated_data):
#         instance.title = validated_data.get('title', instance.title)
#         instance.code = validated_data.get('code', instance.code)
#         instance.linenos = validated_data.get('linenos', instance.linenos)
#         instance.language = validated_data.get('language', instance.language)
#         instance.style = validated_data.get('style', instance.style)
#         instance.save()
#         return instance
"""
HyperlinkedModelSerializer 与 ModelSerializer 有以下区别：
默认情况下不包括 id 字段。
自带一个 url 字段，使用 HyperlinkedIdentityField 。
关联关系使用 HyperlinkedRelatedField 字段类型，而不是
PrimaryKeyRelatedField 字段类型。
"""
class SnippetSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    highlight = serializers.HyperlinkedIdentityField(view_name='snippet-highlight', format='html')
    class Meta:
        model = Snippet
        fields = ['url', 'id', 'highlight', 'title', 'linenos', 'code', 'language', 'style', 'owner']


class UserSerializer(serializers.HyperlinkedModelSerializer):
    # 获得关联用户id的列表
    # snippets为model中user反向关联的snippet
    snippets = serializers.HyperlinkedRelatedField(many=True, view_name='snippet-detail', read_only=True )

    class Meta:
        model = User
        fields = ('url', 'id', 'username', 'snippets')
