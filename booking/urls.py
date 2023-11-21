from django.urls import path
from . import views

app_name = 'booking'

urlpatterns = [
    path('', views.ListRoomsView.as_view(), name='list_rooms'),
    path('create-booking/<int:room_id>', views.CreateBookingView.as_view(),
         name='create_booking'),
    path('my-bookings/', views.ListBookingsView.as_view(),
         name='list_bookings'),
    path('delete-booking/<int:booking_id>/', views.booking_delete_view,
         name='delete_booking')
]
