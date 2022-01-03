from rest_framework.permissions import IsAuthenticated
from rest_framework import routers, serializers, viewsets, views, status
from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   ListModelMixin, UpdateModelMixin, RetrieveModelMixin)
from rest_framework.viewsets import GenericViewSet
from rest_framework.views import APIView
from .serializers import (ProfilRetruteurSerializer, UserSerializer, LoginSerializer, SetpassSerializers, FormationSerializer, CompetenceSerializer, ExperienceSerializer, JobSerializer, ProfilUserSerializer)
from django.contrib.auth import logout, login, authenticate
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import RetrieveAPIView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import (Job, ProfilUser, ProfilRetruteur, Competence, Formation, Experience)
from rest_framework.permissions import BasePermission, IsAuthenticated, AllowAny, SAFE_METHODS


class ProfilRetruteurViewset(RetrieveModelMixin, CreateModelMixin, ListModelMixin,
                    UpdateModelMixin, DestroyModelMixin, GenericViewSet):
    """
    Description: Model Description
    """
    querySet = ProfilRetruteur.objects.all()
    serializer_class = ProfilRetruteurSerializer
    

class AuthViewSet(GenericViewSet):
    """
    Description: Model Description
    """
    serializer_class = LoginSerializer
    permission_classes = [AllowAny, ]

    @swagger_auto_schema(
        request_body=LoginSerializer(),
        operation_description="Check the credentials and return the REST Token if the credentials are valid and authenticated. Calls Django Auth login method to register User ID in Django session framework Accept the following POST parameters: username, password Return the REST Framework Token Object\'s key.")
    @action(methods=["POST"], detail=False)
    def signin(self, request, *args, **kwargs):

        seria = LoginSerializer(data=self.request.data)
        seria.is_valid(raise_exception=True)

        username = seria.validated_data.get('username')
        password = seria.validated_data.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                token = Token.objects.get_or_create(user=user)[0].key

                data = {
                    'message': 'user has logged in successfuly',
                    'email': user.email,
                    'username': user.username,
                }

                res = LoginSerializer(user).data
                return Response(res, status=status.HTTP_200_OK)
            else:

                return Response({
                    'status': 'Unauthorized',
                    'message': 'This account has been disabled.'
                }, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({
                'status': 'Unauthorized',
                'message': 'Username/password combination invalid.'
            }, status=status.HTTP_401_UNAUTHORIZED)

        return JsonResponse(UserSerializer(user).data)


class LogoutView(GenericViewSet):
    permission_classes = [IsAuthenticated,]

    # Logout Ressource

    @swagger_auto_schema(
        operation_description='Calls Django logout method and delete the Token object assigned to the current User object.')
    @action(methods=["POST"], detail=False)
    def post(self, request, format=None):
        user = request.user.username
        print(user)
        request.user.auth_token.delete()
        #        Simple Call on /logout in post. No arguments
        logout(request)

        return Response({'deconnecter': f'bye bye {user}'}, status=status.HTTP_200_OK)


class SetPassword(GenericViewSet):
    permission_classes = [IsAuthenticated, ]
    serializer_class = SetpassSerializers
    
    # Logout Ressource

    @swagger_auto_schema(
        operation_description='Calls Django password reset  method and change the password.')
    @action(methods=["POST"], detail=False)
    def post(self, request, format=None):
        user = request.user.username
        print(user)
        seria = SetpassSerializers(data=self.request.data)
        seria.is_valid(raise_exception=True)

        old_password = seria.validated_data.get('old_password')
        newpassword = seria.validated_data.get('newpassword')

        user = authenticate(username=user, password=old_password)
        if user is not None:
            user.set_password(newpassword)
            user.save()
            login(request,user)
            return Response({'password': f'password has change'}, status=status.HTTP_200_OK)

        return Response({'password': f'password does\'nt match'}, status=status.HTTP_400_BAD_REQUEST)

        #        Simple Call on /logout in post. No arguments
