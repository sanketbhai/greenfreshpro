from django import forms

class SigninForm(forms.Form):
    mail = forms.EmailField(help_text='A valid email address, please.')
    password= forms.CharField(label='password', max_length=100,widget=forms.PasswordInput)

class SignupForm(forms.Form):
    your_name = forms.CharField(label='Your name', max_length=100)
    password= forms.CharField(label='Password', max_length=100,widget=forms.PasswordInput)
    Email=forms.EmailField(help_text='A valid email address, please.')

class ContactForm(forms.Form):
    mail = forms.EmailField(help_text='A valid email address, please.')
    title= forms.CharField(max_length=100)
    Description=forms.CharField(widget=forms.Textarea(attrs={'rows':3, 'cols':21}))

class AdressForm(forms.Form):
    Street = forms.CharField(max_length=100)
    Room_no= forms.IntegerField()
    Pin_code=forms.IntegerField()