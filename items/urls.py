from django.urls import path,include
from . import views

urlpatterns = [
    path('set_discount', views.SetDiscount.as_view()),
    path('set_pizza_discount', views.SetPizzaDiscount.as_view()),
    path('remove_discount', views.RemoveDiscount.as_view()),
    path('remove_pizza_discount', views.RemovePizzaDiscount.as_view()),
    path('get_cities', views.GetCities.as_view()),
    path('get_city', views.GetCity.as_view()),
    path('get_categories', views.GetCategories.as_view()),
    path('get_banners', views.GetBanners.as_view()),
    path('get_items_by_city', views.GetItemsByCity.as_view()),
    path('get_souses_by_city', views.GetSousesByCity.as_view()),
    path('get_item_by_id/<int:pk>', views.GetItemsByID.as_view()),
    path('get_recommended_items', views.GetRecommendedItems.as_view()),
    path('get_recommended_items_for_meat', views.GetRecommendedItemsForMeat.as_view()),
    path('copy_city', views.CopyCity.as_view()),

]
