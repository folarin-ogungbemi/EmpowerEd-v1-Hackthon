from allauth.account.forms import SignupForm
from django.forms import (CharField, TextInput, Textarea,
                          ChoiceField, Select, ModelForm,
                          ModelChoiceField, DateInput)
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import Mentor, Student, Parent


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

        if user.role == 'Student':
            Student.objects.create(user_id=user)
        elif user.role == 'Parent':
            Parent.objects.create(user_id=user)
        elif user.role == 'Mentor':
            Mentor.objects.create(user_id=user)

        return user


class MentorProfileForm(ModelForm):
    class Meta:
        """
        Inner class for metadata options for the form.
        """
        model = Mentor
        fields = ['area_of_expertise', 'bio', 'userpic']

        widgets = {
            'area_of_expertise': TextInput(attrs={
                'placeholder': 'area of expertise'
            }),
            'bio': Textarea(attrs={
                'style': 'height: 150px;',
                'placeholder': ("tell about yourself")
            }),
            'userpic': TextInput(attrs={
            })
        }

    def __init__(self, *args, **kwargs):
        """
        Specifies layout to add image preview.
        """
        super(MentorProfileForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.add_input(Submit('save', 'Save',
                              css_class='btn btn-primary px-5'))


class StudentProfileForm(ModelForm):
    parent = ModelChoiceField(queryset=Parent.objects.all(), required=False)

    class Meta:
        model = Student
        fields = ['date_of_birth', 'interests', 'userpic', 'parent']

        widgets = {
            'date_of_birth': DateInput(attrs={
                'type': 'date',
                'placeholder': 'Date of Birth'
            }),
            'interests': Textarea(attrs={
                'style': 'height: 150px;',
                'placeholder': 'Tell us about yourself'
            }),
            'userpic': TextInput(attrs={
                'placeholder': 'URL of your profile picture'
            })
        }

    def __init__(self, *args, **kwargs):
        """
        Specifies layout to add image preview.
        """
        super(StudentProfileForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.add_input(Submit('save', 'Save',
                              css_class='btn btn-primary px-5'))


class ParentProfileForm(ModelForm):
    class Meta:
        """
        Inner class for metadata options for the form.
        """
        model = Parent
        fields = ['phone_number', 'userpic']

        widgets = {
            'phone_number': TextInput(attrs={
                'placeholder': 'Phone Number',
            }),
            'userpic': TextInput(attrs={
            }),
        }

    def __init__(self, *args, **kwargs):
        """
        Specifies layout to add image preview.
        """
        super(ParentProfileForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.add_input(Submit('save', 'Save',
                              css_class='btn btn-primary px-5'))