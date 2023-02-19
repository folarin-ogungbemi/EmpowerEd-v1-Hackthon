from django.views import generic
from datetime import date, timedelta
from django.contrib.auth import get_user_model
from .models import Mentor, Resource, Parent, Student
from .forms import MentorProfileForm, StudentProfileForm, ParentProfileForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy


class LandingView(generic.TemplateView):
    """
    A view for displaying the Home page.
    """
    template_name = "index.html"


class ResourcesView(generic.ListView):
    template_name = "resources.html"
    model = Resource
    paginate_by = 5


class MentorsView(generic.ListView):
    template_name = "mentors.html"
    model = Mentor
    paginate_by = 8


class AboutView(generic.TemplateView):
    template_name = "about.html"


def calculate_age(date_of_birth):
    today = date.today()
    age = (today.year - date_of_birth.year - ((today.month, today.day)
           < (date_of_birth.month, date_of_birth.day)))
    return age


class UserProfileDetailView(LoginRequiredMixin, generic.DetailView):
    """
    A view for displaying User Profile in details.
    """
    template_name = "profile.html"
    context_object_name = "profile"
    
    def get_queryset(self):
        User = get_user_model()
        user_pk = self.kwargs['pk']
        user = get_object_or_404(User, pk=user_pk)

        if user.role == "Student":
            return Student.objects.all()
        elif user.role == "Parent":
            return Parent.objects.all()
        elif user.role == "Mentor":
            return Mentor.objects.all()
        else:
            return None

    def get_object(self):
        User = get_user_model()
        user_pk = self.kwargs['pk']
        user = get_object_or_404(User, pk=user_pk)

        if user.role == "Student":
            obj = get_object_or_404(Student, user_id=user)
        elif user.role == "Parent":
            obj = get_object_or_404(Parent, user_id=user)
        elif user.role == "Mentor":
            obj = get_object_or_404(Mentor, user_id=user)
        else:
            obj = None
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        User = get_user_model()
        user_pk = self.kwargs['pk']
        user = get_object_or_404(User, pk=user_pk)
        if user.role == "Student":
            context['age'] = calculate_age(user.student.date_of_birth)
            context['student_mentor'] = user.student.relationship_set.all()
            context['student_parent'] = user.student.parent
        elif user.role == "Parent":
            context['parent_student'] = user.parent.student_set.all()
        elif user.role == "Mentor":
            context['mentor_student'] = user.mentor.relationship_set.all()
        return context


class UserProfileUpdateView(LoginRequiredMixin, generic.UpdateView):
    """
    A view for updating a user's profile.
    """
    template_name = "update_profile.html"

    def get_form_class(self):
        """
        Return a different form class based on the user's role
        """
        if self.request.user.role == "Student":
            return StudentProfileForm
        elif self.request.user.role == "Parent":
            return ParentProfileForm
        elif self.request.user.role == "Mentor":
            return MentorProfileForm
        else:
            return UserProfileForm

    def get_object(self):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy('home:profile', kwargs={'pk': self.user.pk})

    def get_queryset(self):
        if self.request.user.role == "Student":
            return Student.objects.all()
        elif self.request.user.role == "Parent":
            return Parent.objects.all()
        elif self.request.user.role == "Mentor":
            return Mentor.objects.all()
        else:
            return None

    def form_valid(self, form):
        """
        Saves the form and returns the
        superclass's form_valid method.
        """
        form.save()
        return super(UserProfileUpdateView, self).form_valid(form)

