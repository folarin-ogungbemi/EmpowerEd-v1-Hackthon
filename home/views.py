from django.views import generic
from .models import Mentor, Resource


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
