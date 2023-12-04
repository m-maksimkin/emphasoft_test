from django.urls import path

from .views import (
    ListRooms,
    CreateBooking,
    BookingList,
    BookingDelete
)

app_name = 'booking'

urlpatterns = [
    path('list-rooms/', ListRooms.as_view(), name='list_rooms'),
    path('create-booking/<int:pk>/',
         CreateBooking.as_view(), name='create-booking'),
    path('my-bookings/', BookingList.as_view(), name='list_bookings'),
    path('delete-booking/<int:pk>',
         BookingDelete.as_view(), name='delete_booking'),
]
