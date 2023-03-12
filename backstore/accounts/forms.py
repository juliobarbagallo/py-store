from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

from .models import Account


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                "This email address is already in use. Please use a different email address."
            )
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
            Account.objects.create(user=user)
        return user


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email"]

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if (
            email
            and User.objects.filter(email=email).exclude(pk=self.instance.pk).exists()
        ):
            raise forms.ValidationError(
                _("This email address is already in use. Please use a different email.")
            )
        return email


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ["phone_number", "address"]
