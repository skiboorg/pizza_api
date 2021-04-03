from django.urls import path,include
from . import views

urlpatterns = [
    path('get_all', views.GetAll.as_view()),

]
