from django.urls import path
from . import views


app_name = "home"


urlpatterns = [
    path('', views.LandingView.as_view(), name='home'),
    path('resources/', views.ResourcesView.as_view(), name='resources'),
    path('mentors/', views.MentorsView.as_view(), name='mentors'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('profile/<pk>', views.UserProfileDetailView.as_view(), name='profile')
]
