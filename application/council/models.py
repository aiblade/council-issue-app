from django.db import models
from django.db import models
from django.conf import settings
from django.urls import reverse


class Issue(models.Model):
    """
    Represents a logged issue in the council reporting system.
    """

    # Enumerated choices for categories:
    ISSUE_CATEGORIES = [
        ('POTHOLE', 'Pothole'),
        ('STREET_LIGHTING', 'Street Lighting'),
        ('GRAFFITI', 'Graffiti'),
        ('ASB', 'Anti-Social Behaviour'),
        ('FLY_TIPPING', 'Fly-Tipping'),
        ('BLOCKED_DRAIN', 'Blocked Drains'),
        ('OTHER', 'Other'),
    ]

    # Enumerated choices for status tracking:
    ISSUE_STATUS = [
        ('OPEN', 'Open'),
        ('IN_PROGRESS', 'In Progress'),
        ('RESOLVED', 'Resolved'),
        ('CLOSED', 'Closed'),
    ]

    title = models.CharField(max_length=200)
    ai_summary = models.TextField()
    description = models.TextField()

    # Use a CharField with choices to keep track of the issue category.
    category = models.CharField(
        max_length=50,
        choices=ISSUE_CATEGORIES,
        default='OTHER'
    )

    email = models.EmailField()

    # The staff member responsible for addressing the issue.
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name='assigned_issues',
        null=True,
        blank=True
    )

    # Track the current status of the issue using the choice field.
    status = models.CharField(
        max_length=20,
        choices=ISSUE_STATUS,
        default='OPEN'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} (Status: {self.get_status_display()})"

    def get_absolute_url(self):
        return reverse('home')
