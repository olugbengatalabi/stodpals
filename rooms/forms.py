from django.forms import ModelForm
from .models import Room
from django.conf import settings



class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        exclude = ['host', 'participants']
        

# class UserForm(ModelForm):
#     class Meta:
#         model = settings.AUTH_USER_MODEL
        
#         fields = ['avatar', 'name', 'username', 'email', 'bio']