from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm, TextInput
from .models import ChatRoom

from users.models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username',)


class ChatRoomCreationForm(ModelForm):
    class Meta:
        model = ChatRoom
        fields = ['room_name', 'second_user']

    def __init__(self, *args, **kwargs):
        super(ChatRoomCreationForm, self).__init__(*args, **kwargs)
        self.fields['room_name'].widget = TextInput(attrs={
            'id': 'room-name',
            'name': 'room-name'
        })

    def clean(self):
        ...
