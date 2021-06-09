from django.urls import path
from django.conf.urls import include


urlpatterns = [
    path('api/', include('users.urls')),
    path('api/', include('init.urls')),
    path('api/', include('posts.urls')),
    path('api/', include('banners.urls')),
]