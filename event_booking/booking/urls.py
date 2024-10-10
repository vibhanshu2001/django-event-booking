from django.urls import path
from .views import signup, login, book_event, event_details, get_all_users, add_event, get_all_events

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('login/', login, name='login'),
    path('book-event/', book_event, name='book-event'),
    path('event/<int:event_id>/', event_details, name='event-details'),
    path('get-users/', get_all_users, name='get-users'),
    path('add-event/', add_event, name='add-event'),
    path('get-events/', get_all_events, name='get-events'),
]
