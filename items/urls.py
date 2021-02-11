from django.urls import path,include
from . import views

urlpatterns = [
    path('get_cities', views.GetCities.as_view()),
    path('get_items_by_city', views.GetItemsByCity.as_view()),
    path('get_souses_by_city', views.GetSousesByCity.as_view()),
    path('get_item_by_id/<int:pk>', views.GetItemsByID.as_view()),




]
