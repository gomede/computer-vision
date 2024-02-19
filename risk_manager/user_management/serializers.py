from django.contrib.auth.models import User
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for Django's built-in User model.
    """
    
    class Meta:
        model = User  # Specify the model to be serialized
        fields = ['id', 'username', 'email', 'password']  # Fields to include in the serialization
        extra_kwargs = {'password': {'write_only': True}}  # Make password write-only for security

    def create(self, validated_data):
        """
        Create and return a new User instance, given the validated data.
        """
        # Use Django's create_user method to handle user creation
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

    def update(self, instance, validated_data):
        """
        Update and return an existing User instance, given the validated data.
        """
        # Update user instance with validated data
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        
        # Check if password is provided and update it using set_password
        if 'password' in validated_data:
            instance.set_password(validated_data['password'])
        
        instance.save()  # Save the updated instance
        return instance
