import threading
import openai
from django.db import transaction
from django.conf import settings
from council.models import Issue


def generate_ai_summary_sync(issue_id):
    """
    Synchronously generates an AI summary for the given issue.
    If the issue description is empty (after trimming), it sets ai_summary to an empty string
    and does not call the OpenAI API.
    :param issue_id: The ID of the issue to generate a summary for.
    """

    try:
        # Set the API key.
        openai.api_key = settings.OPENAI_API_KEY

        with transaction.atomic():
            issue = Issue.objects.select_for_update().get(pk=issue_id) # Lock the row for update.

            # If a summary already exists, do not regenerate.
            if issue.ai_summary:
                return

            # Trim the description.
            description_text = issue.description.strip()
            if description_text == "":
                # For an empty description, ensure the summary remains empty.
                issue.ai_summary = ""
                issue.save(update_fields=['ai_summary'])
                print(f"Issue {issue_id} has no valid description to summarise.")
                return

            # Build the prompt.
            prompt = (
                "Please provide a concise summary of around 10 words for the following issue description:\n\n"
                f"{description_text}\n\nSummary:"
            )
            print(f"Generating summary for issue {issue_id} with prompt:\n{prompt}")

            # Call the OpenAI API.
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that summarises text."},
                    {"role": "user", "content": prompt}
                ],
                timeout=10
            )

            summary = response.choices[0].message.content.strip()
            print(f"Received summary for issue {issue_id}: {summary}")

            # Save the generated summary.
            issue.ai_summary = summary
            issue.save(update_fields=['ai_summary'])
    except Exception as e:
        print(f"Error generating AI summary for issue {issue_id}: {e}")


def generate_ai_summary_async(issue_id):
    """
    Spawns a background thread to run generate_ai_summary_sync.
    :param issue_id: The ID of the issue to generate a summary for.
    """

    thread = threading.Thread(target=generate_ai_summary_sync, args=(issue_id,))
    thread.daemon = True
    thread.start()
