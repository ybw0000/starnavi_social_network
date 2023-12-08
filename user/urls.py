from django.urls import path

from user.views import CreateUserView
from user.views import DecoratedTokenObtainPairView
from user.views import DecoratedTokenRefreshView
from user.views import UserActivityView

urlpatterns = [
    path('signup/', CreateUserView.as_view(), name='signup'),
    path('token/', DecoratedTokenObtainPairView.as_view(), name='signin'),
    path('token/refresh/', DecoratedTokenRefreshView.as_view(), name='refresh-token'),
    path('activity/<str:username>/', UserActivityView.as_view(), name='user-activity'),
]
