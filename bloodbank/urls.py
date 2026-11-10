# which function to call for each page
from django.urls import path
from . import views


urlpatterns = [
    path('',views.home,name='home'),
    path('register/',views.register, name='register'),
    path('search/',views.search_results,name='search_results'),
]