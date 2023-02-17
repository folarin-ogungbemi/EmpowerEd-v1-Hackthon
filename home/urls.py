from django.urls import path
from . import views


app_name = "home"


urlpatterns = [
    path('', views.LandingView.as_view(), name='home'),
]
