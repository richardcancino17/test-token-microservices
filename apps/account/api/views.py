from django.shortcuts import render
from rest_framework import generics, status, filters
from django.utils.decorators import method_decorator
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from .serializers import *
from django.utils.crypto import get_random_string
from rest_framework_jwt.serializers import jwt_payload_handler, \
    jwt_encode_handler
from django.contrib.auth import user_logged_in
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import PageNumberPagination


class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data,
                                         context={"request": request})
        serializer.is_valid(raise_exception=True)
        user_logged_in.send(
            sender=serializer.validated_data.get("user").__class__,
            request=request,
            user=serializer.validated_data.get("user"))
        response_data = {"token": serializer.validated_data.get('token')}
        return Response(response_data, status=status.HTTP_200_OK)
        # token,created=Token.objects.get_or_create(user=serializer.get_user())
        # return Response({'token': token.key}, status=status.HTTP_200_OK)


class CreateUserAPIView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = CreateUserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data,
                                         context={"request": request})
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        payload = jwt_payload_handler(user)
        return Response({'token': jwt_encode_handler(payload)})
        # token, created = Token.objects.get_or_create(user=user)
        # return Response({'token': token.key}, status=status.HTTP_200_OK)


class RetrieveUserAPIView(generics.RetrieveAPIView):
    serializer_class = RetrieveUserSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user


class EmailContactAPIView(generics.GenericAPIView):
    serializer_class = EmailContactSerializer
    permission_classes = AllowAny,

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        random = get_random_string(10),
        serializer.send_mail(random)
        return Response({"details": [{
            'object': 'Successful',
            'message': 'Email sent successfully, check it out in his inbox',
            'random': random
        }]},
            status=status.HTTP_200_OK)
