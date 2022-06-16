from django import forms
from .models import Publication, Author


class AddResearchForm(forms.ModelForm):
    class Meta:
        model = Publication
        fields = '__all__'

class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = '__all__'
