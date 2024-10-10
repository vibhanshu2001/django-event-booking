from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny

from .models import User, Event, UserEventMapping
from .serializers import UserSerializer, EventSerializer, UserEventMappingSerializer

@api_view(['POST'])
def signup(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = User(
            email=serializer.validated_data['email'],
            fname=serializer.validated_data['fname'],
            lname=serializer.validated_data['lname'],
            password=make_password(request.data['password'])
        )
        user.save()
        return Response({'message': 'User created successfully', 'user_id': user.id}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login(request):
    email = request.data.get('email')
    password = request.data.get('password')

    if not email or not password:
        return Response({"error": "Email and password are required."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

    if check_password(password, user.password):
        return Response({"message": "Login successful"}, status=status.HTTP_200_OK)
    else:
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
def book_event(request):
    user_id = request.data.get('user_id')
    event_id = request.data.get('event_id')
    guests = request.data.get('guests')

    if not user_id:
        return Response({'error': 'User ID is required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    try:
        event = Event.objects.get(id=event_id)
    except Event.DoesNotExist:
        return Response({'error': 'Event not found'}, status=status.HTTP_404_NOT_FOUND)

    if guests is None:
        return Response({'error': 'Number of guests is required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        guests = int(guests)
    except ValueError:
        return Response({'error': 'Invalid number of guests'}, status=status.HTTP_400_BAD_REQUEST)

    if event.maximum_allowed_bookings - event.current_bookings >= guests:
        booking = UserEventMapping.objects.create(
            user=user,
            event=event,
            guests=guests
        )

        event.current_bookings += guests
        event.save()
        
        return Response({'message': 'Booking successful!'}, status=status.HTTP_201_CREATED)

    return Response({'error': 'Guests exceed event limit'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def event_details(request, event_id):
    try:
        event = Event.objects.get(id=event_id)
        serializer = EventSerializer(event)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Event.DoesNotExist:
        return Response({'error': 'Event not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def get_all_users(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def add_event(request):
    serializer = EventSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Event added successfully!"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_all_events(request):
    events = Event.objects.all()
    serializer = EventSerializer(events, many=True)
    return Response(serializer.data)