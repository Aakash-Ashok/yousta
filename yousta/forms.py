from django import forms
from yousta.models import *
from django.contrib.auth.forms import UserCreationForm


class RegistrationForm(UserCreationForm):
    class Meta:
        model=User
        fields=["username","email","password1","password2","phone","address"]
class LoginForm(forms.Form):
    username=forms.CharField()
    password=forms.CharField(widget=forms.PasswordInput)


class CategoryCreateForm(forms.ModelForm):
    class Meta:
        model=Category
        fields=["name"]


class ClothAddForm(forms.ModelForm):
    class Meta:
        model=Cloths
        fields="__all__"


class ClothVarientForm(forms.ModelForm):
    class Meta:
     model=ClothVarients
     exclude=("cloth",)


class OfferAddForm(forms.ModelForm):
    class Meta:
        model=Offers
        exclude=("clothvarient",)
        widgets={
            "start_date":forms.DateInput(attrs={"type":"date"}),
            "due_date":forms.DateInput(attrs={"type":"date"})
        }
       

class CartForm(forms.ModelForm):
    class Meta:
        model=Carts
        fields=["clothvarient","status"]
