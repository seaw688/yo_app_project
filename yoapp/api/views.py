from django.shortcuts import render, HttpResponseRedirect
from django.apps import apps
from rest_framework import viewsets
from rest_framework import generics
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
from rest_framework import generics, mixins
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.models import Token

from django.contrib.auth import get_user_model
from django.apps import apps

from .serializers import OfferSerializer, CategorySerializer, ShopSerializer, \
    CustomUserSerializer, LoginSerializer

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.settings import api_settings
from rest_framework.pagination import LimitOffsetPagination

from django.contrib.auth import (
    login as django_login,
    logout as django_logout
)
from django.core.exceptions import ObjectDoesNotExist

from rest_auth.models import TokenModel
from rest_auth.app_settings import create_token



UserModel = get_user_model()
CategoryModel = apps.get_model('common', 'Category')
OfferModel = apps.get_model('yomarket', 'Offer')
ShopModel = apps.get_model('yomarket', 'Shop')


def custom_api_response(serializer=None, content=None, metadata=None):
    if content:
        response = {'metadata': {}, 'content': content}
        return response

    if not hasattr(serializer, '_errors') or len(serializer._errors) == 0:
        if hasattr(serializer, 'data'):
            response = {'metadata': {}, 'content': serializer.data}
        else:
            response = {'metadata': {}, 'content': 'unknown'}
    else:
        response = {'metadata': {}, 'errors': serializer._errors}
    return response



class CategoryList(APIView):
    permission_classes = (AllowAny,)
    #pagination_class = api_settings.DEFAULT_PAGINATION_CLASS
    #print (pagination_class)


    def get(self, request, format=None):
        #paginator = LimitOffsetPagination()
        categories = CategoryModel.objects.all()
        #print (categories)
        #result_page = paginator.paginate_queryset(categories, request)
        serializer = CategorySerializer(categories, many=True) # , context={'request': request}
        #response = Response(serializer.data, status=status.HTTP_200_OK)
        response = Response(custom_api_response(serializer), status=status.HTTP_200_OK)
        return response

    # def get(self, request, pk, format=None):
    #     # user = request.user
    #     event = Event.objects.get(pk=pk)
    #     news = event.get_news_items().all()
    #     paginator = LimitOffsetPagination()
    #     result_page = paginator.paginate_queryset(news, request)
    #     serializer = NewsItemSerializer(result_page, many=True, context={'request': request})
    #     response = Response(serializer.data, status=status.HTTP_200_OK)
    #     return response



class OfferList(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, format=None, pk=None):
        offers = OfferModel.objects.all()
        if pk is not None:
            #offers = get_object_or_404(offers, pk=pk)
            offers = OfferModel.objects.filter(pk=pk).all()
            serializer = OfferSerializer(offers)
        else:
            serializer = OfferSerializer(offers, many=True)
        response = Response(custom_api_response(serializer), status=status.HTTP_200_OK)
        #return Response(serializer.data)
        return response


class ShopList(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, format=None):
        shops = ShopModel.objects.all()
        serializer = ShopSerializer(shops, many=True)
        #return Response(serializer.data)
        return Response(custom_api_response(serializer), status=status.HTTP_200_OK)


class Logout(APIView):
    #queryset = UserModel.objects.all()

    def get(self, request, format=None):
        # simply delete the token to force a login
        try:
            request.user.auth_token.delete()
        except (AttributeError, ObjectDoesNotExist):
            pass

        django_logout(request)

        content = {"detail": "Successfully user logged out"}
        return Response(custom_api_response(None, content), status=status.HTTP_200_OK)
        #return Response({"detail": "Successfully user logged out"}, status=status.HTTP_200_OK)


class UserViewSet(viewsets.ModelViewSet):
    #queryset = UserModel.objects.filter(role='CUSTOMER').all()
    serializer_class = CustomUserSerializer
    permission_classes = (IsAuthenticated,)

    def retrieve(self, request, pk=None):
        #queryset = UserModel.objects.filter(role='CUSTOMER').all()
        #user = get_object_or_404(queryset, pk=pk)
        user = UserModel.objects.filter(role='CUSTOMER', pk=pk).all()
        serializer = CustomUserSerializer(user, many=True)
        #serializer.is_valid()
        response = Response(custom_api_response(serializer), status=status.HTTP_200_OK)
        return response

    def list(self, request, *args, **kwargs):
        users = UserModel.objects.filter(role='CUSTOMER').all()

        # page = self.paginate_queryset(queryset)
        # if page is not None:
        #     serializer = self.get_serializer(page, many=True)
        #     return self.get_paginated_response(serializer.data)
        #serializer = self.get_serializer(queryset, many=True)
        serializer = CustomUserSerializer(users, many=True)

        return Response(custom_api_response(serializer), status=status.HTTP_200_OK)

    #@csrf_exempt
    # def create(self, validated_data):
    #     self.permission_classes = (AllowAny,)
    #     #print (self)
    #     user = super(UserViewSet, self).create(validated_data)
    #     #user.set_password(validated_data['password'])
    #     print (user)
    #     user.save()
    #     return user


@api_view(['POST'])
@permission_classes(())
def register_view(request):
    # обработчик регистрации
    serializer = CustomUserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(custom_api_response(serializer), status=status.HTTP_201_CREATED)
    else:
        return Response(custom_api_response(serializer), status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes(())
def login_view(request):
    #serializer = AuthTokenSerializer(data=request.data)
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        token = create_token(TokenModel, user, serializer)
        #token = Token.objects.get(user=user)
        django_login(request, user)
        content = {'token': token.key, 'email': user.email, 'id': user.id}
        return Response(custom_api_response(serializer, content), status=status.HTTP_200_OK)
        #return Response({'token': token.key, 'username': user.username, 'id': user.id})
    else:
        return Response(custom_api_response(serializer), status=status.HTTP_400_BAD_REQUEST)



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







