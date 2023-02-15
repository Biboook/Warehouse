from django.urls import path

from . import views
from .views import *

urlpatterns = [
    path('', index, name='home'),
    path('authentication/', login, name='auth'),
    path('userpage/', userpage, name='userpage'),
    path('store/', get_store, name='store'),
    path('register/', reg, name='register'),
    path('logout', views.logout_view, name='logout'),
    path('password/', passchange, name='password-change'),
    path('add-store/', addstore, name='addstore'),
    path('add-products/', add_product, name='add_products'),
    path('activate/<uidb64>/<token>', views.activate, name='activate')
]
