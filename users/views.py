import json

from django.contrib.auth.views import LoginView
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.views.generic import TemplateView, CreateView, ListView
from .forms import ChatRoomCreationForm, CustomUserCreationForm
from .models import ChatRoom, ChatMessage


# class MainPaige(TemplateView):
#     template_name = 'main.html'


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


# class Room(TemplateView):
#     template_name = 'room.html'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data()
#         context['username'] = mark_safe(json.dumps(self.request.user.username))
#         context['messages'] = ChatMessage.objects.filter(chat__room_name=self.kwargs['room_name'])
#         return context


class Room(ListView):
    model = ChatMessage
    template_name = 'room.html'
    paginate_by = 15

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(chat__room_name=self.kwargs['room_name']).order_by('created_at')


class Login(LoginView):
    template_name = 'login.html'


class Registration(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'register.html'
    success_url = '/login/'
