from django.urls import path, include
from rest_framework_simplejwt import views as jwt_views
from . import views

urlpatterns = [
    path('token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path("register/", views.UserRegisterationAPIView.as_view(), name="create_user"),
    path("login/", views.UserLoginAPIView.as_view(), name="login_user"),
    path("logout/", views.UserLogoutAPIView.as_view(), name="logout_user"),
]
