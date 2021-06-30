from django.urls import path
from django.conf import settings
from django.conf.urls import include
from django.conf.urls.static import static


urlpatterns = [
    path('api/', include('users.urls')),
    path('api/', include('init.urls')),
    path('api/', include('posts.urls')),
    path('api/', include('banners.urls')),
    path('api/', include('pages.urls')),
    path('api/', include('menus.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
