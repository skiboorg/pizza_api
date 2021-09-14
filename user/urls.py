from django.urls import path,include
from . import views

urlpatterns = [


    path('me/', views.GetUser.as_view()),
    path('update', views.UserUpdate.as_view()),
    path('recover_password', views.UserRecoverPassword.as_view()),
    path('add_address', views.AddAddress.as_view()),
    path('delete_address/<int:pk>', views.DeleteAddress.as_view()),
    path('use_promo', views.UsePromo.as_view()),
    # path('comfirm_phone_step_one', views.ComfirmPhoneStepOne.as_view()),
    path('code_sms', views.SendCodeSMS.as_view()),
    path('change_password', views.ChangePassword.as_view()),
    path('set_n_id', views.SetNId.as_view()),

]
