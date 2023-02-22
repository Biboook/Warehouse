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
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('store/<int:pk>/', views.store_detail, name='store_detail'),
    path('store/<int:pk>/edit/', views.edit_store, name='edit_store'),
    path('store/<int:pk>/delete/', views.delete_store, name='delete_store'),
    path('expense/<int:store_id>/', views.expense_product, name='expense_product'),
    path('expense_history/<int:pk>/', views.expense_history, name='expense_history'),
    path('arrivals_history/', views.arrivals, name='arrivals'),
]
