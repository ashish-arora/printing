__author__ = 'ashish'
from rest_framework_mongoengine.serializers import DocumentSerializer
from .models import User, UserResponse, UserRequest
from rest_framework import serializers

class UserSerializer(DocumentSerializer):

    class Meta:
        model=User
        fields = ('name', 'msisdn', 'email', 'devices', 'country', 'city', 'token', 'type', 'business_name',
                  'description', 'images', 'md', 'ts')

class UserRequestSerializer(DocumentSerializer):

    class Meta:
        model=UserRequest
        fields = ('user_id', 'status', 'type', 'description', 'hired_user', 'ts')

class UserResponseSerializer(DocumentSerializer):

    class Meta:
        model = UserResponse
        fields = ('user_id', 'request_id', 'status', 'response_data', 'quote', 'ts')