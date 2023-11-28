from django.contrib.auth.forms import UserCreationForm
from .models import UserModel
from django import forms

class CustomUserCreationForm(UserCreationForm):
    USER_TYPE_CHOICES = (
    ('Doctor', 'doctor'),
    ('Patient', 'patient') 
    )

    type = forms.ChoiceField(
        choices=USER_TYPE_CHOICES,
        widget=forms.Select(attrs={"class": "form-control"})
    )
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].help_text = ''
        self.fields['username'].help_text=''   
        self.fields['password2'].help_text=''  
    class Meta:
        model=UserModel
        
        fields=('username','userProfile',
                'first_name','last_name','email','type')
          



class LoginForm(forms.Form):
    username = forms.CharField(
        widget= forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control"
            }
        )
    )