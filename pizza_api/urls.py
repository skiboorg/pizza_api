from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/items/', include('items.urls')),
    path('api/cart/', include('cart.urls')),
    path('api/user/', include('user.urls')),
    path('api/order/', include('order.urls')),
    path('api/promotion/', include('promotion.urls')),
    path('api/courier/', include('courier.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
