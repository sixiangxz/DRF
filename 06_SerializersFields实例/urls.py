from django.urls import path
from app1 import views

urlpatterns = [
    path('posts/', views.PostList.as_view(), name='post-list'),
    path('posts/<int:pk>/', views.DetailPost.as_view(), name='post-detail'),
    path('posts/<int:pk>/<str:title>/', views.RetrievePostView().as_view()),
    path('upload/<str:filename>', views.FileUploadView().as_view()),

]