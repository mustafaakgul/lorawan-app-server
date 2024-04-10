from django import forms
from .models import Endnode

class EndnodeForm(forms.ModelForm):
    class Meta:
        model = Endnode
        fields = ["name", "description",   "dev_eui", "app_eui", "dev_add", "net_sess_key", "app_sess_key"]

"""
class EndnodeForm(forms.Form):

    username = forms.CharField(max_length = 50, label = "Username")
    email = forms.CharField(max_length=50, label="Email")
    password = forms.CharField(max_length = 20, label = "Password", widget = forms.PasswordInput)
    confirm = forms.CharField(max_length = 20, label = "Confirm Password", widget = forms.PasswordInput)

    def clean(self):
        username = self.cleaned_data.get("username")
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        confirm = self.cleaned_data.get("confirm")

        if password and confirm and password != confirm:
            # throw exception
            raise forms.ValidationError("Passwords not matched")

        values = {
            "username": username,
            "email" :email,
            "password": password
        }
        return values
"""