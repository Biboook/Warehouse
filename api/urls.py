from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from django.urls import path, include
from djangoProject1 import settings
from website.views import *
from api.views import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

urlpatterns = [
    path('products/', ProductAPIList.as_view()),
    path('stores/<uuid:pk>', StoreAPIList.as_view()),
    path('auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
    path('drf-auth/', include('rest_framework.urls')),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]