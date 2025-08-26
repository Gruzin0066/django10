from django.urls import path
from .views import *

app_name = 'comments'

urlpatterns = [
    path('add/<slug:slug>/', CommentCreateView.as_view(), name='add_comment'),
    path('list/<slug:slug>/', PostCommentsListView.as_view(), name='post_comments'),
    path('moderate/<int:pk>/', moderate_comment, name='moderate_comment'),
]