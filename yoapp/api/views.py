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

from .serializers import OfferSerializer, UserSerializer, CategorySerializer, ShopSerializer

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.settings import api_settings
from rest_framework.pagination import LimitOffsetPagination


UserModel = get_user_model()
CategoryModel = apps.get_model('common', 'Category')
OfferModel = apps.get_model('yomarket', 'Offer')
ShopModel = apps.get_model('yomarket', 'Shop')


class CategoryList(APIView):
    permission_classes = (AllowAny,)
    #pagination_class = api_settings.DEFAULT_PAGINATION_CLASS
    #print (pagination_class)


    def get(self, request, format=None):
        paginator = LimitOffsetPagination()
        categories = CategoryModel.objects.all()
        result_page = paginator.paginate_queryset(categories, request)
        serializer = CategorySerializer(result_page, many=True) # , context={'request': request}
        #print (serializer)
        response = Response(serializer.data, status=status.HTTP_200_OK)
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


# class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
#     permission_classes = (AllowAny,)
#     queryset = CategoryModel.objects.all()
#     serializer_class = CategorySerializer


class OfferList(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, format=None, pk=None):
        #print (request.user)
        offers = OfferModel.objects.all()
        if pk is not None:
            offers = get_object_or_404(offers, pk=pk)
            #print (offers)
            #offers = OfferModel.objects.filter(pk=pk).all()
            serializer = OfferSerializer(offers)
            #print(serializer.is_valid())
            #print (serializer.data)
            #print(serializer.errors)
        else:
            serializer = OfferSerializer(offers, many=True)
        return Response(serializer.data)


class ShopList(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, format=None):
        shops = ShopModel.objects.all()
        serializer = ShopSerializer(shops, many=True)
        return Response(serializer.data)


class Logout(APIView):
    queryset = UserModel.objects.all()

    def get(self, request, format=None):
        # simply delete the token to force a login
        request.user.auth_token.delete()
        return Response({"detail": "Successfully user logged out"}, status=status.HTTP_200_OK)


class UserViewSet(viewsets.ModelViewSet):
    queryset = UserModel.objects.filter(role='CUSTOMER').all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def retrieve(self, request, pk=None):
        queryset = UserModel.objects.filter(role='CUSTOMER').all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = UserSerializer(user)
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







