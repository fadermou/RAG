
from django.contrib import admin
from django.urls import path
from .views import *
from users import *

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    # API endpoints
    path("api/register/", RegisterAPIView.as_view(), name="register-api"),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path("register/", register_page, name="register-page"),
    path("upload/", upload_page, name="upload-page"),
    path("query/", upload_page, name="query-page"),
    path("login/", login_page, name="login-page"),
    path("logout/", logout_page, name="logout-page"),
    path("chat/", login_page, name="chat"),

]

