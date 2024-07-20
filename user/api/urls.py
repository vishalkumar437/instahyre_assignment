from django.urls import path
from user.api.views import RegisterUserView, LoginUserView

urlpatterns = [
    path('register', RegisterUserView.as_view(), name='register'),
    path('login', LoginUserView.as_view(), name='login'),
]