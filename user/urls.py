from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework import routers
from django.urls import path, include
from user.views import (RegisterView, LoginView,
                        GenerateOTP, VerifyOTP, ValidateOTP, DisableOTP, UserViewSet, GroupViewSet)

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)


urlpatterns = [
    path('', include(router.urls)),

    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/register', RegisterView.as_view()),
    path('auth/login', LoginView.as_view()),
    path('auth/otp/generate', GenerateOTP.as_view()),
    path('auth/otp/verify', VerifyOTP.as_view()),
    path('auth/otp/validate', ValidateOTP.as_view()),
    path('auth/otp/disable', DisableOTP.as_view()),
]
