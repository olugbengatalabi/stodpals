from django.forms import ModelForm
from .models import Room
from django.contrib.auth import get_user_model



class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        exclude = ['host', 'participants']
        

# class UserForm(ModelForm):
#     class Meta:
#         model = get_user_model()
        
#         fields = ['avatar', 'name', 'username', 'email', 'bio']