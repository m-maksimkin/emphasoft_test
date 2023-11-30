from .views import SignUpView
from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

app_name = 'accounts'

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', obtain_auth_token, name='login'),
]
