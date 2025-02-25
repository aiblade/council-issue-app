import time
from django.test import TestCase
from unittest.mock import patch, MagicMock
from council.models import Issue
from aisummary.utils import generate_ai_summary_sync, generate_ai_summary_async


class GenerateAISummarySyncTests(TestCase):
    """
    Tests for the generate_ai_summary_sync function.
    """

    @patch('aisummary.utils.openai.ChatCompletion.create') # Mock the OpenAI API call.
    def test_empty_description(self, mock_create):
        """
        For an issue with a whitespace-only description, the function should not call
        the OpenAI API and should set ai_summary to an empty string.
        :param mock_create: MagicMock
        """

        # Create an issue with a whitespace-only description.
        issue = Issue.objects.create(description="   ", ai_summary="")

        # Make sure ai_summary is empty.
        issue.ai_summary = ""
        issue.save(update_fields=['ai_summary'])

        generate_ai_summary_sync(issue.id)

        # Verify that the API was not called.
        mock_create.assert_not_called()

        # Reload the issue and verify that ai_summary is an empty string.
        issue.refresh_from_db()
        self.assertEqual(issue.ai_summary, "")


class GenerateAISummaryAsyncTests(TestCase):
    @patch('aisummary.utils.generate_ai_summary_sync') # Mock the synchronous function.
    def test_async_calls_sync(self, mock_sync):
        """
        Test that generate_ai_summary_async eventually calls generate_ai_summary_sync with the correct issue ID.
        """

        issue = Issue.objects.create(description="Async test description", ai_summary="")
        generate_ai_summary_async(issue.id)

        # Allow a short delay for the background thread to run.
        time.sleep(0.1)
        mock_sync.assert_called_once_with(issue.id) # Verify that the synchronous function was called.
