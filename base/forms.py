from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django import forms
from .models import *

Fgender = [
    ('Male', 'Male'),
    ('Female', 'Female'),
]

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    idCard = forms.CharField(max_length=12, label='ID Card')
    phone = forms.CharField(max_length=10, label='Phone Number')
    gender = forms.ChoiceField(choices=Fgender)
    role = 'Reader'

    def cleaned_id_card(self):
        check_idCard = self.cleaned_data.get('idCard')
        if Profile.objects.filter(idCard=check_idCard).exists():
            raise forms.ValidationError("This ID Card already exists!")
        return check_idCard
    def cleaned_phone(self):
        check_phone = self.cleaned_data.get('phone')
        if Profile.objects.filter(phone=check_phone).exists():
            raise forms.ValidationError("This Phone Number already exists!")
        return check_phone
    def cleaned_mail(self):
        check_mail = self.cleaned_data.get('email')
        if User.objects.filter(email=check_mail).exclude(email=self.cleaned_data.get('email')).exists():
            raise forms.ValidationError("This Email already exists!")
        return check_mail
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'first_name', 'last_name', 'email', 'idCard', 'phone',)
        widgets = {
            'username': forms.TextInput(attrs={'class': 'login'}),
            'password1': forms.PasswordInput(attrs={'class': 'login'}),
            'password2': forms.PasswordInput(attrs={'class': 'login'}),
            'first_name': forms.TextInput(attrs={'class': 'login'}),
            'last_name': forms.TextInput(attrs={'class': 'login'}),
            'email': forms.TextInput(attrs={'class': 'login'}),
            'idCard': forms.TextInput(attrs={'class': 'login'}),
            'phone': forms.TextInput(attrs={'class': 'login'}),
        }

    def save(self, commit=True):
        user = super(CustomUserCreationForm, self).save(commit=False)

        email = user.email

        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.password1 = self.cleaned_data['password1']
        user.password2 = self.cleaned_data['password2']
       

        # if User.objects.filter(email=email).exclude(id=user.id).exists():
        #     raise forms.ValidationError("This Email already exists!")

        if commit:
            user.save()

            profile = Profile.objects.create(user=user)
            profile.role = '3'
            idCard = profile.idCard
            phone = profile.phone
            if Profile.objects.filter(idCard=idCard).exclude(idCard=profile.idCard).exists():
                raise forms.ValidationError("This ID Card already exists!")
            if Profile.objects.filter(phone=phone).exclude(phone=profile.phone).exists():
                raise forms.ValidationError("This Phone Number already exists!")

            profile.save()

        return user

class BookForm(forms.ModelForm):
    authorID = forms.ModelMultipleChoiceField(queryset=Author.objects.all(), label='Author')
    languageID = forms.ModelMultipleChoiceField(queryset=Language.objects.all(), label='Language')
    publisherID = forms.ModelMultipleChoiceField(queryset=Publisher.objects.all(), label='Publisher')


    class Meta:
        model = Book

        fields = (  'bookID',
                    'name',
                    'image',
                    'year',
                    'price',
                    'stock', 
                    'condition',
                    'topicID',
                    'authorID', 
                    'languageID',  
                    'publisherID',
                    'positionID',
                    'description'
        )