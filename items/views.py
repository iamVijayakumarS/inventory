from django.contrib.auth import get_user_model
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import *
from .serializers import ItemSerializer
from rest_framework.permissions import IsAuthenticated
from django.core.cache import cache
import logging

# User model for login and registration
User = get_user_model()

# Logger
logger = logging.getLogger(__name__)

# Logger info
logger.info("User accessed the endpoint")


# Registration view
class RegisterView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        logger.info(f"Attempting to register user: {username}")

        if User.objects.filter(username=username).exists():
            # Added cache to track the user details 
            logger.warning(f"User registration failed: {username} already exists.")
            return Response(
                {"error": "User already exists", "status": status.HTTP_400_BAD_REQUEST},
                status=status.HTTP_400_BAD_REQUEST,
            )
        user = User(username=username)
        user.set_password(password)
        user.save()
        logger.info(f"User registered successfully: {username}")
        return Response(
            {"message": "User registered", "status": status.HTTP_201_CREATED},
            status=status.HTTP_201_CREATED,
        )

# Login view
class LoginView(TokenObtainPairView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        tokens = serializer.validated_data
        response_data = {
            "message": "User authenticated successfully",
            "status": status.HTTP_200_OK,
            "tokens": tokens,
        }
        return Response(response_data, status=status.HTTP_200_OK)


class ItemCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = ItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response_data = {
                "message": "Item created successfully",
                "status": status.HTTP_201_CREATED,
                "item": serializer.data,
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            errors = serializer.errors
            formatted_errors = {
                field: ", ".join(messages) for field, messages in errors.items()
            }
            return Response(
                {
                    "message": "Failed to create User!",
                    "errors": formatted_errors,
                    "status": status.HTTP_400_BAD_REQUEST,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )


class ItemDetailViewOrUpdateOrDelete(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, item_id):
        # Check if item is in cache
        item = cache.get(f'item_{item_id}')
        if item is None:  # If not in cache, retrieve from database
            item = Inventory_Items.objects.filter(id=item_id).first()
            if item is None:
                return Response(
                    {"error": "Item not found", "status": status.HTTP_404_NOT_FOUND},
                    status=status.HTTP_404_NOT_FOUND,
                )
            # Store item in cache for future requests
            cache.set(f'item_{item_id}', item, timeout=60*15)  # Cache for 15 minutes
        
        serializer = ItemSerializer(item)
        return Response(serializer.data)
    
    def put(self, request, item_id):
        item = Inventory_Items.objects.filter(id=item_id).first()
        if item is None:
            return Response(
                {"error": "Item not found", "status": status.HTTP_404_NOT_FOUND},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = ItemSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message": "Item updated successfully",
                    "data": serializer.data,
                    "status": status.HTTP_200_OK,
                },
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, item_id):
            item = Inventory_Items.objects.filter(id=item_id).first()
            if item is None:
                return Response(
                    {"error": "Item not found", "status": status.HTTP_404_NOT_FOUND},
                    status=status.HTTP_404_NOT_FOUND,
                )
            item.delete()
            return Response(
                {"message": "Item deleted", "status": status.HTTP_204_NO_CONTENT},
                status=status.HTTP_204_NO_CONTENT, 
            )


