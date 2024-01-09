from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

class LoginForm(forms.Form):
    username = forms.CharField(label='ชื่อผู้ใช้')
    password = forms.CharField(widget=forms.PasswordInput ,label='รหัสผ่าน')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['phone_number']

        labels = {
            'phone_number': 'หมายเลขโทรศัพท์', 
        }
        widgets = {
            'phone_number': forms.TextInput(attrs={'placeholder': 'กรอกหมายเลขโทรศัพท์', 'class': 'w-full px-3 py-2 border rounded-md text-sm'}),
        }

