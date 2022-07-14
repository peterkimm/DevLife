from django.forms import ModelForm
from .models import Posting

class PostingForm(ModelForm):
    class Meta:
        model = Posting
        fields = ['date', 'status', 'text']