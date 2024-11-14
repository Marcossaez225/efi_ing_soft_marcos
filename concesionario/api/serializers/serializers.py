from django.contrib.auth.models import User
from rest_framework import serializers
from vehicles.models import Brand, Country, Vehicle, FollowedVehicle, Comment, VehicleImage, Client

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['id', 'name']

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['id', 'name']

class VehicleImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleImage
        fields = ['id', 'image', 'is_main']

class VehicleSerializer(serializers.ModelSerializer):
    brand = BrandSerializer(read_only=True)
    country_of_manufacture = CountrySerializer(read_only=True)
    images = VehicleImageSerializer(many=True, read_only=True)
    comments = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Vehicle
        fields = [
            'id', 'brand', 'model', 'year_of_manufacture', 'number_of_doors',
            'engine_displacement', 'fuel_type', 'country_of_manufacture', 
            'price_in_usd', 'images', 'comments'
        ]

class FollowedVehicleSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    vehicle = VehicleSerializer(read_only=True)

    class Meta:
        model = FollowedVehicle
        fields = ['id', 'user', 'vehicle', 'followed_at']

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'user', 'vehicle', 'text', 'created_at', 'updated_at']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email'] 

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']