from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import status
from user.service.service import user_register_service, user_login_service
from rest_framework.authentication import TokenAuthentication
from rest_framework.authentication import (BaseAuthentication, get_authorization_header)
from rest_framework.permissions import IsAuthenticated, AllowAny

class BaseAuthPermissionClass:
    authentication_classes = [
        TokenAuthentication,
    ]
    permission_classes = [
        IsAuthenticated,
    ]

class RegisterUserView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    def post(self, request):
        errors, user = user_register_service(request)
        if len(errors) > 0 and user is None:
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(user, status=status.HTTP_201_CREATED)
    
class LoginUserView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    def post(self, request):
        errors, token = user_login_service(request)
        if len(errors) > 0:
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(token, status=status.HTTP_200_OK)
