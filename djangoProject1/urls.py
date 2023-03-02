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
    path('api/v1/productlist/', ProductAPIList.as_view()),
    path('api/v1/storelist/<int:pk>', StoreAPIUpdate.as_view()),
    path('api/v1/storedelete/<int:pk>', StoreAPIDestroy.as_view()),
    path('api/v1/auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
    path('api/v1/drf-auth/', include('rest_framework.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

