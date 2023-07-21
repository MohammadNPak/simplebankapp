from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.contrib.auth import authenticate



class UserRegisterationSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('username', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = self.Meta.model.objects.create_user(**validated_data)
        return user

class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('username', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, attrs):
        username = attrs.get('username', None)
        password = attrs.get('password', None)
        user=authenticate(username=username,password=password)
        if user is None:
            raise serializers.ValidationError("Invalid username/password")
        elif not user.is_active:
            raise serializers.ValidationError("User is not active")
        return user
        