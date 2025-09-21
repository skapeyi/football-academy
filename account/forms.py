from django import forms


class LoginForm(forms.Form):
    email = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Email",
            "type": "email"
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "Password"
        }),
        required=True
    )
    
    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")

        if not email or not password:
            raise forms.ValidationError("Both fields are required.")

        return cleaned_data
    
    def validate_email(self):
        email = self.cleaned_data.get("email")
        if not email:
            raise forms.ValidationError("Email is required.")
        
        # check email format
        if "@" not in email or "." not in email.split("@")[-1]:
            raise forms.ValidationError("Enter a valid email address.")
        return email
    
    def validate_password(self):
        password = self.cleaned_data.get("password")
        if not password:
            raise forms.ValidationError("Password is required.")
        return password



class RegisterForm(forms.Form):
    email = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Email",
            "type": "email"
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "Password"
        }),
        required=True
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "Confirm Password"
        }),
        required=True
    )
    telephone = forms.CharField(
        max_length=15,
        required=False,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Telephone"
        })
    )
    
    
    def validate_password(self):
        password = self.cleaned_data.get("password")
        if not password:
            raise forms.ValidationError("Password is required.")
        return password
    
    def validate_confirm_password(self):
        confirm_password = self.cleaned_data.get("confirm_password")
        if not confirm_password:
            raise forms.ValidationError("Please confirm your password.")
        # check if passwords match
        if self.cleaned_data.get("password") != confirm_password:
            raise forms.ValidationError("Passwords do not match.")  
        return confirm_password

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")

        return cleaned_data
    
    
    
