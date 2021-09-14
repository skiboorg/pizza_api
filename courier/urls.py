from django.urls import path,include
from . import views

urlpatterns = [
    path('all', views.GetAllCouriers.as_view()),
    path('assign_order', views.AssingOrder.as_view()),
    path('get_courier', views.GetCourier.as_view()),
    path('set_token', views.SetToken.as_view()),
    path('order_in_delivery', views.OrderInDelivery.as_view()),
    path('update_coordinates', views.UpdateCoordinates.as_view()),
    path('get_coordinates', views.GetCoordinates.as_view()),
    path('delivery_complete', views.DeliveryComplete.as_view()),


]
