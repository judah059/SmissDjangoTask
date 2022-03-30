from django.forms import ModelForm, TextInput

from chat.models import ChatRoom


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
