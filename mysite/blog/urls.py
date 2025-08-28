from django.urls import path
from .views import *

urlpatterns = [
    path('', HomePageView.as_view(), name='index'),
    path('category/', CategoryListView.as_view(), name='category'),
    path('about/', AboutPageView.as_view(), name='about'),
    path('category/<slug:slug>/', CategoryPageView.as_view(), name='cat'),
    path('post/<slug:slug>/', PostPageView.as_view(), name='post'),
    # path('tag/<slug:slug>/', show_tags, name='tag'),
    path('tag/<slug:slug>/', PostByTagsListView.as_view(), name='tag'),
    path('add_post/', AddPostView.as_view(), name='add_post'),
    path('edit_post/<slug:slug>/', PostEditPage.as_view(), name='edit_post'),
    path('delete_post/<slug:slug>/', PostDeletePage.as_view(), name='delete_post'),
]