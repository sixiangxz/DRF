from .models import User, Topic, Post
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):

    class Meta:

        model = User
        fields = ('id', 'username', )

class TopicSerializer(serializers.ModelSerializer):

    class Meta:
        model = Topic
        fields = ('id', 'name', )


class PostSerializer(serializers.ModelSerializer):
    # 如果想在post序列化的时候同时序列化user,则可以添加下面内容（DRF不主张这样）但是可以满足这样的需求
    # DRF的规范，一个名词url只处理一个资源。不在嵌套的字段关系中同时创建对象
    user = UserSerializer()  # 嵌套关系，user的处理使用UserSerializer来序列化

    class Meta:
        model = Post
        fields = ('id', 'title', 'content', 'user', 'topics')

    # post时候使用
    def create(self, validated_data):

        # 健壮性需考虑
        topic_data = []
        if validated_data['topics']:
            topic_data = validated_data.pop('topics')

        # print(validated_data)
        # {'title': '飞流直下三千尺', 'content': 'bbbbbbbbbbb', 'user': OrderedDict([('username', 'k2k')])}
        user_data = validated_data.pop('user')
        # flag表示创建还是获取对象
        user, flag = User.objects.get_or_create(username=user_data['username'])
        post = Post.objects.create(user=user, **validated_data)
        # 因为提供topics是以列表提供的
        if topic_data:
            post.topics.add(*topic_data)
        return post

    # 修改/更新时候使用
    def update(self, instance, validated_data):
        # 获取topic内容，user的内容，validated_data内容
        # 逐一拿取各条数据 如 instance.title = validated_data.get('title', instance.title)
        # instance.save()
        # instance.user = validated_data.get('user', instance.user)
        # user.save()
        pass
