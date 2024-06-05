from django.urls import path
from  . import views


urlpatterns = [
    path('', views.laptop),
    path('contact', views.send_spam),
    path('searchLaptop', views.searchLaptop, name='searchLaptop'),
   
]