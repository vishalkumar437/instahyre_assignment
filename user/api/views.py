import logging
from rest_framework import generics, status
from rest_framework.response import Response
from user.service.service import user_register_service, user_login_service
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RegisterUserView(generics.GenericAPIView):
    """
    View for registering a new user.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        """
        Handle POST request to register a new user.
        """
        logger.info("Received request to register a new user")
        errors, user = user_register_service(request)
        if len(errors) > 0 and user is None:
            logger.warning("User registration failed with errors: %s", errors)
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        logger.info("User registered successfully: %s", user)
        return Response(user, status=status.HTTP_201_CREATED)

class LoginUserView(generics.GenericAPIView):
    """
    View for logging in an existing user.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        """
        Handle POST request to log in a user.
        """
        logger.info("Received request to log in a user")
        errors, token = user_login_service(request)
        if len(errors) > 0:
            logger.warning("User login failed with errors: %s", errors)
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        logger.info("User logged in successfully, token: %s", token)
        return Response(token, status=status.HTTP_200_OK)
