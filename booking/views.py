from .models import Room, Booking
from .forms import SortRoomsForm, BookingCreateForm

from django.contrib import messages
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST


class ListRoomsView(ListView):
    model = Room
    template_name = 'booking/list_rooms.html'
    context_object_name = 'rooms_list'
    paginate_by = 50
    sort_form = None

    def get_queryset(self):
        queryset = self.model.objects.all()
        self.sort_form = SortRoomsForm(self.request.GET)
        if self.sort_form.is_valid():
            cl = self.sort_form.cleaned_data
            ordering = cl.get('ordering')
            start_date, end_date = cl.get('start_date'), cl.get('end_date')
            if start_date and end_date:
                booked_rooms = self.model.objects.filter(
                    booking__start_date__lte=end_date,
                    booking__end_date__gte=start_date
                )
                queryset = queryset.exclude(id__in=booked_rooms)
            if ordering:
                queryset = queryset.order_by(ordering)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sort_form'] = self.sort_form
        return context


class CreateBookingView(LoginRequiredMixin, FormView):
    form_class = BookingCreateForm
    template_name = 'booking/create_booking.html'
    success_url = reverse_lazy('booking:list_bookings')

    def form_valid(self, form):
        booking = form.save(commit=False)
        room = get_object_or_404(Room, pk=self.kwargs.get('room_id'))
        booking.room, booking.user = room, self.request.user
        if booking.is_valid():
            booking.save()
            messages.success(self.request, 'Комната успешно забронирована.')
        else:
            messages.error(self.request, 'В эти даты комната уже забронирована.')
            return render(self.request, self.template_name,
                          {'form': form}, status=400)
        return super().form_valid(form)


class ListBookingsView(LoginRequiredMixin, ListView):
    model = Booking
    template_name = 'booking/list_bookings.html'
    context_object_name = 'bookings_list'
    paginate_by = 50

    def get_queryset(self):
        queryset = Booking.objects.prefetch_related()\
            .filter(user=self.request.user)
        return queryset


@login_required
@require_POST
def booking_delete_view(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    booking.delete()
    messages.success(request, 'Бронирование успешно удалено')
    return redirect('booking:list_bookings')
