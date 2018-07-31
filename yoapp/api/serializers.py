from rest_framework import serializers
from django.apps import apps
from django.contrib.auth import get_user_model
from django.conf import settings
#from common.models import User, Category

UserModel = get_user_model()
CategoryModel = apps.get_model('common', 'Category')
OfferModel = apps.get_model('yomarket', 'Offer')
ShopModel = apps.get_model('yomarket', 'Shop')


class UserSerializer(serializers.HyperlinkedModelSerializer):

    password = serializers.CharField(write_only=True)

    class Meta:
        model = settings.AUTH_USER_MODEL
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'password')

    def create(self, validated_data):
        user = UserModel(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        #user.save()
        return user


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = CategoryModel
        fields = ('id', 'category_name', 'parent')


class OfferSerializer(serializers.ModelSerializer):

    class Meta:
        model = OfferModel
        fields = ('id', 'category', 'shop', 'title', 'image', 'short_description',
                  'description', 'price', 'discount', 'discount_type', 'code_data')


class ShopSerializer(serializers.ModelSerializer):

    class Meta:
        model = ShopModel
        fields = ('id', 'user', 'title', 'address')

