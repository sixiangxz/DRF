from django.contrib import admin
from django.urls import path, include

from rest_framework.schemas import get_schema_view
schema_view = get_schema_view(title="哈哈")
urlpatterns = [

    path('', include('snippets.urls')),
    path('admin/', admin.site.urls),
    # API 概要
    path('schema/', schema_view),
    path('api-auth/', include('rest_framework.urls')),

]
