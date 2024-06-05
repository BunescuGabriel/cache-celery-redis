from django.urls import path
from  . import views


urlpatterns = [
    path('', views.telefon),
    path('about', views.about),
    path('search', views.search, name='search'),
    path('cos', views.cos),
    path('add_to_cart/<int:phone_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:phone_id>/', views.remove_to_cart, name='remove_to_cart'),
    
    path('checkout/', views.checkout, name='checkout'),
    path('success/', views.success, name='success'),
    
]