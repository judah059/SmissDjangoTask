from django.contrib.auth.views import LoginView
from django.views.generic import CreateView
from .forms import CustomUserCreationForm


class Login(LoginView):
    template_name = 'login.html'


class Registration(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'register.html'
    success_url = '/login/'
