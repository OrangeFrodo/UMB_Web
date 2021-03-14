from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from phonenumber_field.formfields import PhoneNumberField
from .models import Customer, OrderItem


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=150, help_text='Email')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2',)



class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control m-1 col-lg-12',
        'placeholder': 'Krstné meno',
        'aria-label' : "Recipient's username", 
        'aria-describedby' : "basic-addon2"
    }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control m-1 col-lg-12',
        'placeholder': 'Priezvisko',
        'aria-label' : "Recipient's username", 
        'aria-describedby' : "basic-addon2"
    }))
    phone = PhoneNumberField(widget=forms.TextInput(attrs={
        'class': 'form-control m-1 col-lg-12',
        'placeholder': '+421910455866',
        'aria-label' : "Recipient's username", 
        'aria-describedby' : "basic-addon2"
    }))

    class Meta:
        model = Customer
        fields = ('first_name', 'last_name', 'phone',)


class CouponForm(forms.Form):
    code = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control m-1 input-code',
        'placeholder': 'Promo code',
        'aria-label' : "Recipient's username", 
        'aria-describedby' : "basic-addon2"
    }))

class RefundForm(forms.Form):
    Kód_objednávky = forms.CharField()
    Správa = forms.CharField(widget=forms.Textarea)
    Email = forms.EmailField()


class ContactForm(forms.Form):
    meno = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'class': 'form-control m-1 col-lg-12',
        'placeholder': 'Vaše meno',
        'aria-label' : "Recipient's username", 
        'aria-describedby' : "basic-addon2"
    }))
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={
        'class': 'form-control m-1 col-lg-12',
        'placeholder': 'Vaše meno',
        'aria-label' : "Recipient's username", 
        'aria-describedby' : "basic-addon2"
    }))
    Správa = forms.CharField(widget=forms.Textarea(attrs={
        'rows':3,
        'class': 'form-control m-1 col-lg-12',
        }), required=True)
