from rest_framework import serializers
from django.apps import apps
from django.contrib.auth import get_user_model
from django.conf import settings


UserModel = get_user_model()
CategoryModel = apps.get_model('common', 'Category')
OfferModel = apps.get_model('yomarket', 'Offer')
ShopModel = apps.get_model('yomarket', 'Shop')


class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)

    class Meta:
        model = UserModel
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'password')

    def create(self, validated_data):
        user = UserModel(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        #user.save()
        return user


class OwnerUserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)

    class Meta:
        model = UserModel
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
    shop = serializers.StringRelatedField()
    category = serializers.StringRelatedField()

    class Meta:
        model = OfferModel
        fields = ('id', 'category', 'shop', 'title', 'image', 'short_description',
                  'description', 'price', 'discount', 'discount_type', 'code_data')


class ShopSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = ShopModel
        fields = ('id', 'title', 'address', 'user')

    # def to_representation(self, instance):
    #     # instance is the model object. create the custom json format by accessing instance attributes normaly
    #     # and return it
    #     identifiers = dict()
    #     identifiers['id'] = instance.id
    #     identifiers['title'] = instance.title
    #
    #     representation = {
    #         'identifiers': identifiers,
    #         #'user_id': instance.user_id,
    #         'address': instance.address
    #     }
    #
    #     return representation

