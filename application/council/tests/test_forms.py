from django.test import TestCase
from council.forms import IssueForm, EditForm
from council.models import Issue
from django.contrib.auth import get_user_model

User = get_user_model()


class IssueFormTest(TestCase):
    def test_issue_form_valid_data(self):
        """
        Test that IssueForm is valid when provided with proper data.
        """

        form_data = {
            "title": "Street Light Issue",
            "description": "The street light is flickering.",
            "category": "STREET_LIGHTING",
            "email": "test@example.com",
        }
        form = IssueForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_issue_form_missing_title(self):
        """
        Test that IssueForm is invalid when the title is missing.
        """

        form_data = {
            "title": "",
            "description": "The street light is flickering.",
            "category": "STREET_LIGHTING",
            "email": "test@example.com",
        }
        form = IssueForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("title", form.errors)


class EditFormTest(TestCase):
    def setUp(self):
        # Create a user and an Issue instance for testing EditForm.

        self.user = User.objects.create_user(username='tester', password='password')
        self.issue = Issue.objects.create(
            title="Graffiti on Wall",
            ai_summary="",
            description="Graffiti needs cleaning.",
            category="GRAFFITI",
            email="graffiti@example.com",
            status="OPEN"
        )

    def test_edit_form_valid_data(self):
        """
        Test that EditForm is valid with correct data.
        """

        form_data = {
            "title": "Graffiti on Wall - Updated",
            "ai_summary": "AI-generated summary",
            "description": "Graffiti cleaned up.",
            "category": "GRAFFITI",
            "email": "graffiti@example.com",
            "assigned_to": self.user.pk,
            "status": "RESOLVED",
        }
        form = EditForm(data=form_data, instance=self.issue)
        self.assertTrue(form.is_valid())

    def test_edit_form_invalid_data(self):
        """
        Test that EditForm is invalid if required fields are missing.
        """

        form_data = {
            "title": "",
            "ai_summary": "AI-generated summary",
            "description": "Graffiti cleaned up.",
            "category": "GRAFFITI",
            "email": "graffiti@example.com",
            "assigned_to": self.user.pk,
            "status": "RESOLVED",
        }
        form = EditForm(data=form_data, instance=self.issue)
        self.assertFalse(form.is_valid())
        self.assertIn("title", form.errors)
