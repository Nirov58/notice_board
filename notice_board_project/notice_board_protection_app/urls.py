from django.urls import path

from .views import Responses, accept, reject

urlpatterns = [
    path('', Responses.as_view(), name='responses'),
    path('<int:pk>/accept', accept, name='accept'),
    path('<int:pk>/reject', reject, name='reject')
]
