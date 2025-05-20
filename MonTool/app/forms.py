from typing import Dict
from django import forms

from django.contrib.auth.password_validation import validate_password
import logging

from app.models import MonUser, Server, Profile

logger = logging.getLogger("django_web")


class SignUpForm(forms.ModelForm):
    """
    Form for user registration.

    Includes password validation, confirmation, and email uniqueness check.
    """

    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control"}))

    class Meta:
        model = MonUser
        fields = ["email", "password"]
        widgets = {
            "email": forms.TextInput(attrs={"class": "form-control"}),
            "password": forms.PasswordInput(attrs={"class": "form-control"})
        }

    def clean(self) -> Dict[str, str]:
        """
        Validates password and checks for password confirmation match.
        """
        password = self.cleaned_data["password"]
        confirm_password = self.cleaned_data["confirm_password"]
        try:
            validate_password(password)
        except Exception as e:
            self.add_error("password", e)
            logger.error("Forms-Signup: The password is not validated")
        if password != confirm_password:
            self.add_error("confirm_password", "Password mismatch! Please check the password in both fields.")
            logger.error("Forms-Signup: Password mismatch")
        logger.info("Forms-Signup: The password was validated")
        return self.cleaned_data

    def clean_email(self) -> str:
        """
        Checks if the provided email already exists.
        """
        email = self.cleaned_data["email"]
        if MonUser.objects.filter(email__contains=email).exists():
            self.add_error("email", "The email inserted is already used! "
                                    "Please sign in or use a different email for sign up.")
            logger.error("Forms-Signup: The email inserted is already used")
        logger.info("Forms-Signup: The email was validated")
        return email


class LogInForm(forms.Form):
    """
    Form for user login with email and password fields.
    """

    email = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control"}))

    def clean_email(self) -> str:
        """
        Validates if the email is registered.
        """
        email = self.cleaned_data["email"]
        if not MonUser.objects.filter(email__contains=email).exists():
            self.add_error("email", "Email is not registered. Please check and try again.")
            logger.error("Forms-Login: Email is not registered")
        logger.info("Forms-Login: Email was validated")
        return email


class ServerCreateForm(forms.ModelForm):
    """
    Form for creating a server entry with OS selection.
    """

    class Meta:
        model = Server
        fields = ["server_name", "user_name", "server_ip", "password"]
        widgets = {
            "server_name": forms.TextInput(attrs={"class": "form-control"}),
            "user_name": forms.TextInput(attrs={"class": "form-control"}),
            "server_ip": forms.TextInput(attrs={"class": "form-control"}),
            "password": forms.PasswordInput(attrs={"class": "form-control"})
        }

    def __init__(self, *args, **kwargs):
        """
        Adds an OS name selection field to the form.
        """
        super().__init__(*args, **kwargs)
        self.fields["os_name"] = forms.ChoiceField(choices=[("Windows", "Windows"), ("Linux", "Linux")],
                                                   widget=forms.Select(attrs={"class": "form-control"}))


class ServerEditForm(forms.ModelForm):
    """
    Form for editing server details.
    """

    class Meta:
        model = Server
        fields = ["server_name", "user_name", "server_ip", "password"]
        widgets = {
            "server_name": forms.TextInput(attrs={"class": "form-control"}),
            "user_name": forms.TextInput(attrs={"class": "form-control"}),
            "server_ip": forms.TextInput(attrs={"class": "form-control"}),
            "password": forms.PasswordInput(attrs={"class": "form-control"})
        }

    def __init__(self, *args, **kwargs):
        """
        Adds an OS name selection field to the form.
        """
        super().__init__(*args, **kwargs)
        self.fields["os_name"] = forms.ChoiceField(choices=[("Windows", "Windows"), ("Linux", "Linux")],
                                                   widget=forms.Select(attrs={"class": "form-control"}))


class ProfileForm(forms.ModelForm):
    """
    Form for creating a user profile.
    """

    class Meta:
        model = Profile
        fields = "__all__"
        exclude = ["user"]
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "bio": forms.TextInput(attrs={"class": "form-control"}),
            "birth_date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "photo": forms.FileInput(attrs={"class": "form-control"})
        }


class EditProfileForm(forms.ModelForm):
    """
    Form for editing a user profile.
    """

    class Meta:
        model = Profile
        fields = "__all__"
        exclude = ["user"]
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "bio": forms.TextInput(attrs={"class": "form-control"}),
            "birth_date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "photo": forms.FileInput(attrs={"class": "form-control"})
        }
