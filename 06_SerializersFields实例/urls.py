from . import views

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"users", views.UserViewSet, basename='user')
router.register(r"topics", views.TopicViewSet, basename='topics')
router.register(r"post", views.PostViewSet, basename='posts')

urlpatterns = router.urls

