from django.urls import path
from .views import PostListview,PostDetailview,PostCreativeview,PostUpdateview,PostDeleteview
from .import views

urlpatterns = [
    path('', PostListview.as_view(),name='blog-home'),
    path('post/<int:pk>', PostDetailview.as_view(),name='post_detail'),
    path('post/new', PostCreativeview.as_view(),name='post_create'),
    path('post/<int:pk>/update', PostUpdateview.as_view(), name='post_update'),
    path('post/<int:pk>/delete', PostDeleteview.as_view(), name='post_delete'),
    path('about', views.about,name='blog-about'),
]


