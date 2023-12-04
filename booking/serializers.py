from rest_framework import serializers

from .models import Room, Booking


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['id', 'name', 'price', 'capacity']


class BookingSerializer(serializers.ModelSerializer):
    room = RoomSerializer(read_only=True)

    class Meta:
        model = Booking
        fields = ['id', 'start_date', 'end_date', 'room']

    def create(self, validated_data):
        booking = Booking(**validated_data)
        if booking.is_valid():
            booking.save()
        else:
            raise serializers.ValidationError(
                "The room is already occupied for this dates"
            )
        return booking

