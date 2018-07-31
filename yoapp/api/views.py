from django.shortcuts import render, HttpResponseRedirect
from django.apps import apps
from rest_framework import viewsets
from rest_framework import generics
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
#from rest_framework.authentication import SessionAuthentication, BaseAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.views import LoginView


from django.contrib.auth import logout, login
from django.http import HttpResponseRedirect
from django.urls import reverse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import generics, mixins
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.models import Token


from common.models import User, Category

from . import serializers

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

class Logout(APIView):
    queryset = User.objects.all()

    def get(self, request, format=None):
        # simply delete the token to force a login
        request.user.auth_token.delete()
        return Response({"detail": "Successfully user logged out."}, status=status.HTTP_200_OK)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter(role='CUSTOMER').all()
    serializer_class = serializers.UserSerializer

    permission_classes = (IsAuthenticated,)

    def retrieve(self, request, pk=None):
        queryset = User.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = serializers.UserSerializer(user)
        return Response(serializer.data)

    #@csrf_exempt
    # def create(self, validated_data):
    #     self.permission_classes = (AllowAny,)
    #     #print (self)
    #     user = super(UserViewSet, self).create(validated_data)
    #     #user.set_password(validated_data['password'])
    #     print (user)
    #     user.save()
    #     return user



# class UserDetail(viewsets.ModelViewSet):
#     """
#     API endpoint that represents a single user.
#     """
#     #model = User
#     #queryset = User.objects.filter(id = pk).first()
#     queryset = User.objects.all()
#     serializer_class = serializers.UserSerializer
#
#
#
# class UserCreateView(generics.CreateAPIView):
#     serializer_class = serializers.UserSerializer



#@method_decorator(csrf_exempt, name='dispatch')
# class UserLoginView(LoginView):
#
#     @method_decorator(csrf_exempt)
#     def dispatch(self, request, *args, **kwargs):
#         print (request, *args, **kwargs)
#         print ('UserLoginView')
#         return super(UserLoginView, self).dispatch(request, *args, **kwargs)

    # print('here')
    # pass



class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = (AllowAny,)
    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer





# from rest_framework.authtoken.models import Token
#
#
# def create_auth_token(sender, instance=None, created=False, **kwargs):
#     # Действие, рассчитанное на сигнал после создания записи пользователя.
#     # Таким образом создаем ему автоматически токен.
#     # Для этого нужно подключить rest_framework.authtoken в INSTALLED_APPS.
#     if created:
#         Token.objects.create(user=instance)