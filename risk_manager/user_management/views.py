from rest_framework import viewsets, status
from rest_framework.response import Response
from django.contrib.auth.models import User
from .serializers import UserSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

class UserViewSet(viewsets.ViewSet):
    """
    A ViewSet for viewing and editing user instances.
    """
    permission_classes = [IsAuthenticated]

    def create(self, request):
        """
        Create a new user instance.
        """
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg_success': 'User created successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        """
        List all users.
        """
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """
        Retrieve a user by id.
        """
        user = User.objects.get(id=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def update(self, request, pk=None):
        """
        Update a user instance.
        """
        user = User.objects.get(id=pk)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg_success': 'User updated successfully'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        """
        Delete a user instance.
        """
        user = User.objects.get(id=pk)
        user.delete()
        return Response({'msg_success': 'User deleted successfully'})

class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Custom view to obtain token pair (access and refresh tokens) with custom claims.
    """
    serializer_class = TokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests to obtain token pair.
        """
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        return Response({
            'Token_renovation': serializer.validated_data.get('refresh'),
            'Token_access': serializer.validated_data.get('access')
        })

class LogoutAPIView(APIView):
    """
    API View to handle logout by blacklisting the refresh token.
    """
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        """
        Handle POST request to logout a user by blacklisting their refresh token.
        """
        try:
            refresh_token = request.data.get("Token_renovation")
            token = RefreshToken(refresh_token)
            token.blacklist()
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        return Response({"Msg_logout_success": "Logout successfully."}, status=status.HTTP_200_OK)
