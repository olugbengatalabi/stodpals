

from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from rooms import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('rooms/', include('rooms.urls')),
    path('api/', include('api.urls')),
    path('', views.index, name = "index"),
    path('accounts/', include('allauth.urls')),
]+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)