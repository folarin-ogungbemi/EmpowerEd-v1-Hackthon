from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin


class MessagesView(LoginRequiredMixin, generic.TemplateView):
    template_name = "messages.html"

    def get_context_data(self, **kwargs):
        return {
                'id': self.request.user.pk
            }
