# user_management/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, CustomTokenObtainPairView, LogoutAPIView
from rest_framework_simplejwt.views import TokenRefreshView

# Initialize the Default Router and register the UserViewSet
router = DefaultRouter()
router.register(r'user', UserViewSet, basename='user')

urlpatterns = [
    # Include all URLs from the router as the root in /api/
    # This automatically generates URLs for the UserViewSet actions (create, list, retrieve, update, delete)
    path('', include(router.urls)),

    # URL for obtaining a new token pair (access and refresh tokens)
    path('authentication/login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),

    # URL for refreshing an existing access token using a refresh token
    path('authentication/renovate/', TokenRefreshView.as_view(), name='token_refresh'),

    # URL for logging out by blacklisting the refresh token
    path('authentication/logout/', LogoutAPIView.as_view(), name='logout'),   
]
