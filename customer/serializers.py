from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from .models import *
User = get_user_model()


class CreateUserFromBc(serializers.Serializer):
    email = serializers.CharField(
        label="E-Mail",
        write_only=True
    )
    password = serializers.CharField(
        label="Password",
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )
    
class LoginSerializers(serializers.Serializer):
    username = serializers.CharField(
        label="Username",
        write_only=True
    )
    password = serializers.CharField(
        label="Password",
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )

    def validate(self, attrs):
        username = attrs.get('username').lower()
        password = attrs.get('password')

        if username and password:
            user = authenticate(request=self.context.get('request'),
                                username=username, password=password)
            if not user:
                msg = 'Access denied: wrong username or password.'
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = 'Both "username" and "password" are required.'
            raise serializers.ValidationError(msg, code='authorization')
        attrs['user'] = user
        return attrs


class OtpSerializer(serializers.Serializer):
    otp = serializers.CharField(
        label='otp',
        write_only=True
    )


class User_list_Serializers(serializers.Serializer):
    class Meta:
        model = User
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # fields = ['customer_id', 'name', 'email', 'password', 'addressLine1',
        #   'addressLine2', 'city', 'postalCode', 'phoneNumber']
        fields = "__all__"
        # extra_kwargs = {'password': {'write_only': True}}
