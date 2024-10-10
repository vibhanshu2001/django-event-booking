from rest_framework import serializers
from .models import User, Event, UserEventMapping

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'fname', 'lname', 'created_at', 'updated_at']

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'event_name', 'event_date', 'maximum_allowed_bookings', 'created_at', 'updated_at']

class UserEventMappingSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserEventMapping
        fields = ['id', 'user', 'event', 'booking_date', 'guests']