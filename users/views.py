import json

from django.contrib.auth.views import LoginView
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.views.generic import TemplateView, CreateView, ListView
from .forms import ChatRoomCreationForm, CustomUserCreationForm
from .models import ChatRoom


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


class Room(TemplateView):
    template_name = 'room.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['username'] = mark_safe(json.dumps(self.request.user.username))
        return context


class Login(LoginView):
    template_name = 'login.html'


class Registration(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'register.html'
    success_url = '/login/'
