from django.urls import path
from api.viewsfolder.usermanagement_views import UserRegisterView,UserLoginView,UserProfileView,ChangeUserPassword,SendResetPasswordEmail,UserPasswordResetView,UsermanagementList
from api.viewsfolder import usermanagement_views as views

urlpatterns = [
   path('userlogin/',UserLoginView.as_view(),name='userdata3'),
    path('userregister/',UserRegisterView.as_view(),name='userdata3'),
    path('userprofile/',UserProfileView.as_view(),name='userdata3'),
     path('changepassword/',ChangeUserPassword.as_view(),name="change_password"),
    path('send-reset-password-email/',SendResetPasswordEmail.as_view(),name="send-reset-password-email"),
    path('reset-password/<uid>/<token>/',UserPasswordResetView.as_view(),name="reset-password"),
    path('usermanagementlist/',UsermanagementList.as_view(),name="reset-password"),
    path('usermanagementupdate/',views.usermanagementupdate,name="reset-password"),
    
]
