from allauth.account.forms import SignupForm
from django.forms import CharField, TextInput


class CustomSignUpForm(SignupForm):
    """
    Custom sign up form.
    """
    first_name = CharField(max_length=30, label='First Name', required=True,
                           widget=TextInput(attrs={'placeholder': 'First Name',
                                            'class': 'form-control'}))
    last_name = CharField(max_length=30, label='Last Name', required=True,
                          widget=TextInput(attrs={'placeholder': 'Last Name',
                                           'class': 'form-control'}))

    def save(self, request):
        user = super(CustomSignUpForm, self).save(request)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()
        return user

