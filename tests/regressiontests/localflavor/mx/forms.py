from django.forms import ModelForm
from models import MXPersonProfile

class MXPersonProfileForm(ModelForm):
    """docstring for MXPersonProfileForm"""
    class Meta:
        model = MXPersonProfile
