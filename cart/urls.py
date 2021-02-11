from django.urls import path,include
from . import views

urlpatterns = [
    path('get_cart', views.GetCart.as_view()),
    path('add_to_cart', views.AddToCart.as_view()),
    path('delete_item', views.DeleteItem.as_view()),
    path('add_item_quantity', views.AddItemQuantity.as_view()),
    path('remove_item_quantity', views.RemoveItemQuantity.as_view()),
    path('erase_cart/<str:session_id>', views.DelCartItems.as_view()),
    path('add_to_cart_constructor', views.AddToCartConstructor.as_view()),
    path('delete_cart_constructor', views.DeleteCartConstructor.as_view()),
    path('add_constructor_quantity', views.AddConstructorQuantity.as_view()),
    path('remove_constructor_quantity', views.RemoveConstructorQuantity.as_view()),
    path('add_to_cart_souse', views.AddToCartSouse.as_view()),
    path('delete_cart_souse', views.DeleteCartSouse.as_view()),
    path('add_souse_quantity', views.AddSouseQuantity.as_view()),
    path('remove_souse_quantity', views.RemoveSouseQuantity.as_view()),
]
