from django.urls import path
from .views import (
    RegisterView,
    ProfileView,
    EmailTokenObtainPairView,
    EmailTokenRefreshView,
    forgot_password,
    reset_password,
)

urlpatterns = [
    path('register', RegisterView.as_view(), name='register'),
    path('login', EmailTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', EmailTokenRefreshView.as_view(), name='token_refresh'),
    path('profile', ProfileView.as_view(), name='profile'),
    path('forgot-password', forgot_password, name='forgot_password'),
    path('reset-password', reset_password, name='reset_password'),
]


