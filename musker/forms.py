from django import forms
from .models import Tweep

class TweepForm(forms.ModelForm):
    body = forms.CharField(required=True,
        widget= forms.widgets.Textarea(
            attrs={
            "placeholder": "Enter your Tweep!",
            "class":"form-control",
            }
            ),  

            label="",                          
                        
        )
    
    class Meta:
        model = Tweep
        exclude = ("User",)
    