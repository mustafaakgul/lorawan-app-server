from django import forms

class RegisterForm(forms.Form):

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

class LoginForm(forms.Form):
    username = forms.CharField(label="Username")
    password = forms.CharField(label="Password", widget=forms.PasswordInput)