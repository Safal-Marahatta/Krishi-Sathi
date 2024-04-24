from django import forms

class loginform(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'placeholder': 'Enter your username'})
    )
    # phone_number=forms.CharField(max_length=10,widget=forms.TextInput(attrs={'placeholder': 'phone number'}))
    password=forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'password'}))


class user_post(forms.Form):
    post_text=forms.CharField(label="say something....",widget=forms.Textarea,required=True)
    post_image=forms.FileField(required=False)

class RegistrationForm(forms.Form):
    first_name=forms.CharField(max_length=30,widget=forms.TextInput(attrs={'placeholder': 'Enter your first name'}))
    last_name=forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={'placeholder':'Enter your last name'})
    )
    username=forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter your name'}))
    occupation=forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter your occupation'}))
    phone_number =forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Enter phone number'})
    )
    email= forms.EmailField(max_length=100,
        widget=forms.EmailInput(attrs={'placeholder': 'Enter your email'}),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter your password'})
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm your password'})
    )
    profile_image=forms.FileField(label='Upload Profile Picture', required=False)
    # years_of_farming_experience=forms.CharField(required=False)



class CropPredictionForm(forms.Form):
    crop = forms.CharField(max_length=100)
    image = forms.ImageField()

