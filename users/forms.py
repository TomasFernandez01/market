from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'phone_number')  # ← QUITÉ username
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Hacer el password más fácil de entender
        self.fields['password1'].help_text = "Mínimo 8 caracteres."
        self.fields['password2'].help_text = "Repite la misma contraseña."

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'phone_number', 'profile_picture')

# MANTENÉ TUS FORMS ORIGINALES, SOLO SIMPLIFICÁ:
class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'profile_picture']
        widgets = {
            'profile_picture': forms.FileInput(attrs={'class': 'form-control'}),
        }

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['profile_picture', 'date_of_birth', 'bio']  # ← Este está BIEN

# AGREGÁ ESTE FORM SIMPLIFICADO PARA REGISTRO FÁCIL:
class SimpleRegistrationForm(forms.ModelForm):
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirmar Contraseña', widget=forms.PasswordInput)
    
    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name')  # ← Solo lo esencial
    
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Las contraseñas no coinciden")
        return password2
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user