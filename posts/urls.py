from django.urls import path

from posts.views import AnalyticsView
from posts.views import CreateListPostView
from posts.views import LikePostView
from posts.views import RetrievePostView

urlpatterns = [
    path('posts/', CreateListPostView.as_view(), name='create-list-post'),
    path('posts/<int:pk>/', RetrievePostView.as_view(), name='retrieve-post'),
    path('posts/<int:pk>/like/', LikePostView.as_view(), name='like-post'),
    path('analytics/', AnalyticsView.as_view(), name='analytics'),
]
