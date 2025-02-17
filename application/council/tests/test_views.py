from django.test import TestCase
from django.urls import reverse
from council.models import Issue
from django.contrib.auth import get_user_model
from unittest.mock import patch

User = get_user_model()


class IssuesViewTest(TestCase):
    def setUp(self):
        # Create some Issue instances.

        Issue.objects.create(
            title="Issue 1",
            ai_summary="",
            description="Description for issue 1.",
            category="POTHOLE",
            email="user1@example.com"
        )
        Issue.objects.create(
            title="Issue 2",
            ai_summary="",
            description="Description for issue 2.",
            category="ASB",
            email="user2@example.com"
        )

    def test_issues_view_status_code(self):
        """
        Test that the IssuesView (home page) returns status code 200.
        """

        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_issues_view_template_used(self):
        """
        Test that the home page uses the 'home.html' template.
        """

        response = self.client.get(reverse('home'))
        self.assertTemplateUsed(response, "home.html")

    def test_issues_view_context_contains_issues(self):
        """
        Test that the context passed to the template contains all issues.
        """

        response = self.client.get(reverse('home'))
        self.assertIn('object_list', response.context)
        self.assertEqual(len(response.context['object_list']), 2)


class IssueDetailViewTest(TestCase):
    def setUp(self):
        # Create an Issue instance for testing the detail view.

        self.issue = Issue.objects.create(
            title="Detail Issue",
            ai_summary="",
            description="Issue for detail view.",
            category="BLOCKED_DRAIN",
            email="detail@example.com"
        )

    def test_issue_detail_view_status_code(self):
        """
        Test that IssueDetailView returns status code 200 for a valid issue.
        """

        response = self.client.get(reverse('issue-detail', kwargs={'pk': self.issue.pk}))
        self.assertEqual(response.status_code, 200)

    def test_issue_detail_view_template_used(self):
        """
        Test that IssueDetailView uses the 'issue_details.html' template.
        """

        response = self.client.get(reverse('issue-detail', kwargs={'pk': self.issue.pk}))
        self.assertTemplateUsed(response, "issue_details.html")


class CreateIssueViewTest(TestCase):
    def setUp(self):
        # Set up the URL for the CreateIssueView.

        self.create_url = reverse('create-issue')

    def test_create_issue_view_get(self):
        """
        Test that the CreateIssueView returns status code 200 on GET.
        """

        response = self.client.get(self.create_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "create_issue.html")

    @patch('council.views.generate_ai_summary_async')
    def test_create_issue_view_post(self, mock_generate_ai_summary_async):
        """
        Test that posting valid data to CreateIssueView creates a new Issue 
        and calls generate_ai_summary_async with the new issue's ID.
        """

        form_data = {
            "title": "New Issue",
            "description": "New issue description.",
            "category": "FLY_TIPPING",
            "email": "newissue@example.com",
        }
        response = self.client.post(self.create_url, data=form_data)
        self.assertEqual(response.status_code, 302)
        issue = Issue.objects.get(title="New Issue")
        mock_generate_ai_summary_async.assert_called_once_with(issue.id)


class UpdateIssueViewTest(TestCase):
    def setUp(self):
        # Create a user and an Issue instance for testing the UpdateIssueView.

        self.user = User.objects.create_user(username="editor", password="password")
        self.issue = Issue.objects.create(
            title="Update Issue",
            ai_summary="",
            description="Original description.",
            category="OTHER",
            email="update@example.com",
            status="OPEN"
        )
        self.update_url = reverse('update-issue', kwargs={'pk': self.issue.pk})

    def test_update_issue_view_get(self):
        """
        Test that the UpdateIssueView returns status code 200 on GET.
        """

        response = self.client.get(self.update_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "update_issue.html")

    def test_update_issue_view_post(self):
        """
        Test that posting valid data to UpdateIssueView updates the Issue.
        """

        form_data = {
            "title": "Updated Issue Title",
            "ai_summary": "Updated AI summary.",
            "description": "Updated description.",
            "category": "ASB",
            "email": "update@example.com",
            "assigned_to": self.user.pk,
            "status": "IN_PROGRESS",
        }
        response = self.client.post(self.update_url, data=form_data)
        self.assertEqual(response.status_code, 302)
        self.issue.refresh_from_db()
        self.assertEqual(self.issue.title, "Updated Issue Title")
        self.assertEqual(self.issue.ai_summary, "Updated AI summary.")
        self.assertEqual(self.issue.description, "Updated description.")
        self.assertEqual(self.issue.category, "ASB")
        self.assertEqual(self.issue.assigned_to, self.user)
        self.assertEqual(self.issue.status, "IN_PROGRESS")


class DeleteIssueViewTest(TestCase):
    def setUp(self):
        # Create an Issue instance for testing the DeleteIssueView.

        self.issue = Issue.objects.create(
            title="Delete Issue",
            ai_summary="",
            description="Issue to be deleted.",
            category="GRAFFITI",
            email="delete@example.com"
        )
        self.delete_url = reverse('delete-issue', kwargs={'pk': self.issue.pk})

    def test_delete_issue_view_get(self):
        """
        Test that the DeleteIssueView returns status code 200 on GET.
        """

        response = self.client.get(self.delete_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "delete_issue.html")

    def test_delete_issue_view_post(self):
        """
        Test that posting to DeleteIssueView deletes the Issue.
        """

        response = self.client.post(self.delete_url)
        self.assertEqual(response.status_code, 302)
        with self.assertRaises(Issue.DoesNotExist):
            Issue.objects.get(pk=self.issue.pk)
