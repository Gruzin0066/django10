from django.urls import path
from .views import *

urlpatterns = [
    path('', HomePageView.as_view(), name='index'),
    path('category/', CategoryListView.as_view(), name='category'),
    path('about/', AboutPageView.as_view(), name='about'),
    path('category/<slug:slug>/', CategoryPageView.as_view(), name='cat'),
    path('post/<slug:slug>/', PostPageView.as_view(), name='post'),
    path('tag/<slug:slug>/', show_tags, name='tag'),
]