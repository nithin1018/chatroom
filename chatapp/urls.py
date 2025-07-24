from django.urls import path,include
from .views import MessageListCreateView,RegisterProfileView
from rest_framework_simplejwt.views import(
    TokenObtainPairView,
    TokenRefreshView
)
urlpatterns = [
    path("messages/<str:room_name>/",MessageListCreateView.as_view(),name="message_list_create"),
    path('create/profile/',RegisterProfileView.as_view(),name='create_profile'),
    path('login/',TokenObtainPairView.as_view(),name='login'),
    path('token/refresh/',TokenRefreshView.as_view(),name='token_refresh'),
]
