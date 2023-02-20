"""
Tests for views.py of main app.
"""
import datetime
from unittest.mock import patch, MagicMock, Mock
from django.test import TestCase, RequestFactory, Client
from django.http import HttpRequest, HttpResponse
from django.urls import reverse
from .views import (calculate_age, UserProfileDetailView,
                    UserProfileUpdateView)
from .models import User, Mentor, Student, Parent, Relationship


class TestCalculateAge(TestCase):

    def test_calculate_age(self):
        date_of_birth = datetime.date(2000, 1, 1)
        age = calculate_age(date_of_birth)
        self.assertEqual(age, 23)

        date_of_birth = datetime.date(1980, 6, 30)
        age = calculate_age(date_of_birth)
        self.assertEqual(age, 42)

        date_of_birth = datetime.date.today()
        age = calculate_age(date_of_birth)
        self.assertEqual(age, 0)
