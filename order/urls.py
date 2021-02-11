from django.urls import path,include
from . import views

urlpatterns = [
    path('new_order', views.NewOrder.as_view()),

]
