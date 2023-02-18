from django.views import generic
from .models import Mentor, Resource, Parent, Student
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404


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