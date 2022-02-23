from django.views.generic import TemplateView


class MainPaige(TemplateView):
    template_name = 'main.html'


class Room(TemplateView):
    template_name = 'room.html'
