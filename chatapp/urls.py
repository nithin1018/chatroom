from django.urls import path,include
from .views import MessageListCreateView,RegisterProfileView,MyTokenObtainPairView,RoomListView
from rest_framework_simplejwt.views import(
    TokenRefreshView
)
urlpatterns = [
    path("messages/<str:room_name>/",MessageListCreateView.as_view(),name="message_list_create"),
    path("room_list/",RoomListView.as_view(),name="room_list"),
    path('create/profile/',RegisterProfileView.as_view(),name='create_profile'),
    path('login/',MyTokenObtainPairView.as_view(),name='login'),
    path('token/refresh/',TokenRefreshView.as_view(),name='token_refresh'),
]
