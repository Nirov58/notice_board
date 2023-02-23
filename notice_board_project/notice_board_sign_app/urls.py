from django.urls import path
from django.contrib.auth.views import LogoutView

from .views import BaseSignUp, check_otc, RestrictedLoginView


urlpatterns = [
    path('signup/', BaseSignUp.as_view(template_name='sign/sign_up.html'), name='sign_up'),
    path('signup/confirm', check_otc, name='sign_up_otc'),
    path('signin/', RestrictedLoginView.as_view(template_name='sign/sign_in.html'), name='sign_in'),
    path('signout/', LogoutView.as_view(template_name='sign/sign_out.html'), name='sign_out'),
]
