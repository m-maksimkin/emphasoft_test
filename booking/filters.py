from django_filters import FilterSet, OrderingFilter, DateFromToRangeFilter

from .models import Room


class RoomFilter(FilterSet):
    date_range = DateFromToRangeFilter(method='filter_date_range')
    ordering = OrderingFilter(
        fields=(
            ('price', 'price'),
            ('capacity', 'capacity'),
        )
    )

    class Meta:
        model = Room
        fields = ['name']

    def filter_date_range(self, queryset, name, value):
        start_date = value.start
        end_date = value.stop
        if start_date and end_date:
            booked_rooms = Room.objects.filter(
                bookings__start_date__lte=end_date,
                bookings__end_date__gte=start_date
            )
            return queryset.exclude(id__in=booked_rooms)
        return queryset.none()
