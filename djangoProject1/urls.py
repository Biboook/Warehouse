from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from django.urls import path, include
from djangoProject1 import settings
from website.views import *
from api.views import *


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('website.urls')),
    path('api/v1/', include('api.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

