from django.views import generic


class LandingView(generic.TemplateView):
    """
    A view for displaying the Home page.
    """
    template_name = "index.html"
