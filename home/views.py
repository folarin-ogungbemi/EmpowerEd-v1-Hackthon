from django.views import generic
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


class MentorsView(generic.ListView):
    template_name = "mentors.html"
    model = Mentor
    paginate_by = 8


class AboutView(generic.TemplateView):
    template_name = "about.html"


class UserProfileDetailView(LoginRequiredMixin, generic.DetailView):
    """
    A view for displaying User Profile in details.
    """
    template_name = "profile.html"
    context_object_name = "profile"

    def get_queryset(self):
        if self.request.user.role == "Student":
            return Student.objects.all()
        elif self.request.user.role == "Parent":
            return Parent.objects.all()
        elif self.request.user.role == "Mentor":
            return Mentor.objects.all()
        else:
            return None

    def get_object(self):
        queryset = self.get_queryset()
        if queryset is not None:
            obj = get_object_or_404(queryset, user_id=self.request.user)
            return obj
        else:
            return None


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

