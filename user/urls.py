from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.urls import path, include
from user.views import (RegisterView, LoginView,
                        GenerateOTP, VerifyOTP, ValidateOTP, DisableOTP)


urlpatterns = [
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/register', RegisterView.as_view()),
    path('auth/login', LoginView.as_view()),
    path('auth/otp/generate', GenerateOTP.as_view()),
    path('auth/otp/verify', VerifyOTP.as_view()),
    path('auth/otp/validate', ValidateOTP.as_view()),
    path('auth/otp/disable', DisableOTP.as_view()),
]
