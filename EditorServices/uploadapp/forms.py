

from django import forms
from uploadapp.models import BgFileToolModel

class BgFileContentForm(forms.ModelForm):

    class Meta:
        model = BgFileToolModel

        exclude = []
        
        file = forms.FileField(
            label='Input File data'
        
    )
