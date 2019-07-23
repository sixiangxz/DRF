from rest_framework import permissions
# 自定义权限
class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
    # 允许任何请求进行读取
    # 所以我们总是允许GET，HEAD或OPTIONS请求。
        if request.method in permissions.SAFE_METHODS:
            return True
    # 只有该snippet的所有者才允许写权限。
    # 别告诉我你读不懂这句代码和这里的if/else逻辑
        return obj.owner == request.user
