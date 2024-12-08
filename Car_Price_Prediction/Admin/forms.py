from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Username'}
        )
    )

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Password'}
        )
    )

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            # Try to authenticate the user
            self.user_cache = authenticate(username=username, password=password)
            
            # Check authentication result
            if self.user_cache is None:
                # Different error messages for different scenarios
                try:
                    # Check if username exists
                    from django.contrib.auth.models import User
                    user = User.objects.get(username=username)
                    # Username exists, so password must be wrong
                    raise forms.ValidationError(
                        "Invalid password. Please try again.",
                        code='invalid_password'
                    )
                except User.DoesNotExist:
                    # Username doesn't exist
                    raise forms.ValidationError(
                        "Invalid username. The username does not exist.",
                        code='invalid_username'
                    )
            elif not self.user_cache.is_active:
                # User account is disabled
                raise forms.ValidationError(
                    "This account is inactive.",
                    code='inactive_account'
                )

        return self.cleaned_data

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']
        required = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']

    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'First Name'}
        ),
        max_length=30,
        required=True
    )

    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Last Name'}
        ),
        max_length=30,
        required=True
    )

    username = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Username'}
        ),
        max_length=30,
        help_text="Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only."
    )

    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={'class': 'form-control', 'placeholder': 'Email'}
        ),
        max_length=254,
        help_text="Required. Enter a valid email address.",
        validators=[validate_email]
    )

    password1 = forms.CharField(    
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Password'}
        ),
        help_text=(
            "Your password must be at least 8 characters long, "
            "contain at least one uppercase letter, "
            "one lowercase letter, and one number."
        )
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}
        ),
        help_text="Enter the same password as above, for verification."
    )

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise ValidationError("A user with this username already exists.")
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError("A user with this email already exists.")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        # Additional password validation
        if password1 and password2:
            if password1 != password2:
                raise ValidationError("Passwords do not match.")
            
            # Additional password strength checks
            if len(password1) < 8:
                raise ValidationError("Password must be at least 8 characters long.")
            
            if not any(char.isupper() for char in password1):
                raise ValidationError("Password must contain at least one uppercase letter.")
            
            if not any(char.islower() for char in password1):
                raise ValidationError("Password must contain at least one lowercase letter.")
            
            if not any(char.isdigit() for char in password1):
                raise ValidationError("Password must contain at least one number.")

        return password2