from django.contrib.auth.models import User, Group
from django.utils import timezone
from rest_framework import serializers

from guestbook_app.models import Message


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['created_at', 'subject', 'name', 'message']

    created_at = serializers.DateTimeField(format="%m/%d/%y %H:%M:%S", read_only=True, default=timezone.now)

    def create(self, validated_data):
        instance = Message(created_at=timezone.now(), **validated_data)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.subject = validated_data.get('subject', instance.subject)
        instance.message = validated_data.get('message', instance.message)
        instance.created_at = validated_data.get('created_at', instance.created_at)
        instance.save()
        return instance

    def validate(self, data):
        if 'name' not in data:
            raise serializers.ValidationError("name is required")
        elif 'message' not in data:
            raise serializers.ValidationError("message is required")
        elif 'subject' not in data:
            raise serializers.ValidationError("subject is required")
        return data

    def validate_subject(self, value):
        """
        Check that the message post is about Django.
        """
        if value == '':
            raise serializers.ValidationError("Title cannot be empty")
        return value

    def validate_name(self, value):
        """
        Check that the message post is about Django.
        """
        if value == '':
            raise serializers.ValidationError("Name cannot be empty")
        return value

    def validate_message(self, value):
        """
        Check that the message post is about Django.
        """
        if value == '':
            raise serializers.ValidationError("Message cannot be empty")
        return value
