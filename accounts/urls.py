from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from .views import SignUpView

app_name = 'accounts'

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', obtain_auth_token, name='login'),
]
