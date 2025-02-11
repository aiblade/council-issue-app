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

    @patch('aisummary.utils.openai.ChatCompletion.create')
    def test_successful_summary_generation(self, mock_create):
        """
        For an issue with a valid description, the function should call the OpenAI API
        once with a prompt containing the description and update ai_summary with the returned text.
        """

        # Set up a fake API response.
        fake_summary = "This is a concise summary."
        fake_message = MagicMock()
        fake_message.content = fake_summary
        fake_choice = MagicMock()
        fake_choice.message = fake_message
        fake_response = MagicMock(choices=[fake_choice])
        mock_create.return_value = fake_response

        # Create an issue with a description.
        description_text = "This is a detailed description that should be summarised."
        issue = Issue.objects.create(description=description_text, ai_summary="")

        # Make sure ai_summary is empty.
        issue.ai_summary = ""
        issue.save(update_fields=['ai_summary'])

        generate_ai_summary_sync(issue.id)

        # Verify that the API call was made exactly once.
        mock_create.assert_called_once()

        # Check that the prompt sent to the API contains the original description.
        _, call_kwargs = mock_create.call_args
        messages = call_kwargs.get("messages", [])
        self.assertTrue(
            any(description_text in message.get("content", "") for message in messages),
            "The prompt sent to the API does not contain the issue description."
        )

        # Reload the issue and verify that ai_summary is updated to the fake summary.
        issue.refresh_from_db()
        self.assertEqual(issue.ai_summary, fake_summary)


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
