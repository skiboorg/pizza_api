from django.urls import path,include
from . import views

urlpatterns = [
    path('new_order', views.NewOrder.as_view()),
    path('pay_success', views.pay_success),
    path('pay_fail', views.pay_fail),

]
