from allauth.account.forms import SignupForm
from django.forms import CharField, TextInput, ChoiceField, Select


class CustomSignUpForm(SignupForm):
    """
    Custom sign up form.
    """
    ROLES = (
        ('Mentor', 'Mentor'),
        ('Student', 'Student'),
        ('Parent', 'Parent'),
    )
    first_name = CharField(max_length=30, label='First Name', required=True,
                           widget=TextInput(attrs={'placeholder': 'First Name',
                                            'class': 'form-control'}))
    last_name = CharField(max_length=30, label='Last Name', required=True,
                          widget=TextInput(attrs={'placeholder': 'Last Name',
                                           'class': 'form-control'}))
    role = ChoiceField(choices=ROLES, label='Role', required=True,
                       widget=Select(attrs={'class': 'form-control'}))

    def save(self, request):
        user = super(CustomSignUpForm, self).save(request)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.role = self.cleaned_data['role']
        user.save()
        return user

