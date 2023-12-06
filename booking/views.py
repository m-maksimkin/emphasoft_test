from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.generics import ListAPIView, DestroyAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Room, Booking
from .permissions import IsOwnerOrSuperuser
from .serializers import RoomSerializer, BookingSerializer
from .filters import RoomFilter


class CustomPagination(PageNumberPagination):
    page_size = 25
    page_size_query_param = 'page_size'
    max_page_size = 100


class ListRooms(ListAPIView):
    """
    Return a list of all rooms and apply filtering based on query params.
    """
    serializer_class = RoomSerializer
    pagination_class = CustomPagination
    filterset_class = RoomFilter
    queryset = Room.objects.all()


class CreateBooking(APIView):
    """
    Create a new booking instance.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, pk, *args, **kwargs):
        room = get_object_or_404(Room, pk=pk)
        serializer = BookingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(room=room, user=request.user)
            return Response(
                serializer.data, status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )


class BookingList(ListAPIView):
    """
    Return a list of all bookings for a user.
    """
    serializer_class = BookingSerializer
    pagination_class = CustomPagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Booking.objects.select_related('room').filter(user=user)


class BookingDelete(DestroyAPIView):
    """
    Delete a booking.
    """
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrSuperuser]
    queryset = Booking.objects.all()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        data = self.get_serializer(instance).data
        self.perform_destroy(instance)
        return Response(data, status=status.HTTP_200_OK)
