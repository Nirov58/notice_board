from django.urls import path
from .views import *


urlpatterns = [
    path('', PostList.as_view(), name='post_list'),
    path('create/', PostCreate.as_view(), name='post_create'),
    path('<int:pk>/', PostItem.as_view(), name='post_item'),
    path('<int:pk>/edit/', PostEdit.as_view(), name='post_edit'),
    path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
    path('<int:pk>/respond/', PostRespond.as_view(), name='post_respond'),
    path('category/<int:pk>/', PostsInCategory.as_view(), name='post_category'),
    path('category/<int:pk>/subscribe/', subscribe, name='category_subscribe'),
    path('category/<int:pk>/unsubscribe/', unsubscribe, name='category_unsubscribe'),
]
