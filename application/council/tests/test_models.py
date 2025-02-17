from django.test import TestCase
from django.urls import reverse
from council.models import Issue


class IssueModelTest(TestCase):
    def setUp(self):
        # Create an Issue instance for testing.

        self.issue = Issue.objects.create(
            title="Broken Street Light",
            ai_summary="",
            description="The street light on 5th Avenue is broken.",
            category="STREET_LIGHTING",
            email="user@example.com"
        )

    def test_str_representation(self):
        """
        Test that the string representation of an Issue includes the title 
        and the human-readable status.
        """

        expected_str = f"{self.issue.title} (Status: {self.issue.get_status_display()})"
        self.assertEqual(str(self.issue), expected_str)

    def test_get_absolute_url(self):
        """
        Test that get_absolute_url returns the URL resolved by reverse('home').
        """

        self.assertEqual(self.issue.get_absolute_url(), reverse('home'))

    def test_default_values(self):
        """
        Test that the default category and status are set properly.
        """

        issue = Issue.objects.create(
            title="Pothole Issue",
            ai_summary="",
            description="A pothole in the road",
            email="another@example.com"
        )
        self.assertEqual(issue.category, "OTHER")
        self.assertEqual(issue.status, "OPEN")
