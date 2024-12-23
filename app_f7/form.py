from django.forms import ModelForm
from app_f7.models import *

class ProfileForm(ModelForm):
    class Meta:
        model = s_profile
        fields = '__all__'

