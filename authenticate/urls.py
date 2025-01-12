from django.urls import path
from .views import RegisterView ,OTPLoginView,UserDetailAPIView
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('auth-token/', obtain_auth_token, name='generate_auth_token'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/',OTPLoginView.as_view(),name='login'),
    path('me/', UserDetailAPIView.as_view(), name='me'),

]