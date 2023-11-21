from .models import Room, Booking

from django.contrib import admin


class BookingAdminInline(admin.TabularInline):
    model = Booking
    extra = 1


class RoomAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "capacity")
    list_filter = ("price", "capacity")
    search_fields = ("name",)
    inlines = (BookingAdminInline,)


class BookingAdmin(admin.ModelAdmin):
    list_display = ("user", "room", "start_date", "end_date")
    list_filter = ("room", "start_date", "end_date")
    search_fields = ("user__username", "room__name")
    readonly_fields = ('created',)


admin.site.register(Room, RoomAdmin)
admin.site.register(Booking, BookingAdmin)
