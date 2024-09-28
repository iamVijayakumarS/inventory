from django.urls import path
from rest_framework_simplejwt.views import  TokenRefreshView
from .views import *

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),  # Registration route
    path("login/", LoginView.as_view(), name="login"),  # Login route
    path(
        "token/refresh/", TokenRefreshView.as_view(), name="token_refresh"
    ),  # Endpoint for refreshing tokens
    path("items/", ItemCreateView.as_view(), name="item-create"),  # To create an item
    path("items/<int:item_id>/",
         ItemDetailViewOrUpdateOrDelete.as_view(), name="item-read"),
]
