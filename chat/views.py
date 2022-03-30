import json

from django.db.models import Q
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.views.generic import CreateView, ListView
from chat.forms import ChatRoomCreationForm
from chat.models import ChatRoom, ChatMessage


class ChatRoomCreateView(CreateView):
    form_class = ChatRoomCreationForm
    template_name = 'main.html'

    def get_success_url(self):
        return reverse('room', kwargs={'room_name': self.object.room_name})

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.first_user = self.request.user
        obj.save()
        return super().form_valid(form=form)


class ChatRoomListView(ListView):
    model = ChatRoom
    template_name = 'main.html'
    extra_context = {'form': ChatRoomCreationForm()}

    def get_queryset(self):
        qs = super().get_queryset()
        first_owner = Q(first_user=self.request.user)
        second_owner = Q(second_user=self.request.user)
        return qs.filter(first_owner | second_owner)


class Room(ListView):
    model = ChatMessage
    template_name = 'room.html'
    paginate_by = 15

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['room_name'] = mark_safe(json.dumps(self.kwargs['room_name']))
        return context

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(chat__room_name=self.kwargs['room_name']).order_by('created_at')




