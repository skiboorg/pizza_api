from django.urls import path,include
from . import views

urlpatterns = [
    path('new_order', views.NewOrder.as_view()),
    path('pay_success', views.pay_success),
    path('pay_fail', views.pay_fail),
    path('stats', views.Stats.as_view()),
    path('get_orders', views.GetOrders.as_view()),
    path('set_order_view', views.SetOrderView.as_view()),
    path('get_user_orders', views.GetUserOrders.as_view()),

]
