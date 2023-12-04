from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.exceptions import ValidationError


class Room(models.Model):
    name = models.CharField(max_length=100, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    capacity = models.PositiveIntegerField()

    class Meta:
        ordering = ('price',)

    def __str__(self):
        return self.name


class Booking(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="bookings"
    )
    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        related_name='bookings'
    )
    start_date = models.DateField()
    end_date = models.DateField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created',)

    def is_valid(self):
        """
        Check if the booking is valid based on room availability.
        """
        if self.start_date > self.end_date:
            return False
        if self.start_date < timezone.now().date():
            return False
        bookings = Booking.objects.filter(room=self.room)
        for booking in bookings:
            if (booking.start_date <= self.start_date <= booking.end_date
                    or booking.start_date <= self.end_date <= booking.end_date):
                return False
            elif (self.start_date <= booking.start_date
                    and self.end_date >= booking.end_date):
                return False
        return True

    def save(self, *args, **kwargs):
        if self.is_valid():
            super().save(*args, **kwargs)
        else:
            raise ValidationError("Booking dates are not available")
