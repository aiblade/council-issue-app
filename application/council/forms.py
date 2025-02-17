from django import forms
from .models import Issue


class IssueForm(forms.ModelForm):
    """
    The form for creating a new issue.
    """

    class Meta:
        """
        The meta class for the IssueForm.
        """

        model = Issue
        fields = ["title", "description", "category", "email"]

        # Define the widgets for the form fields.  
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control", "placeholder": "Issue title"}),
            "category": forms.Select(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "placeholder": "Detailed description of the issue"}),
            "email": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter your email address here"})
        }


class EditForm(forms.ModelForm):
    """
    The form for editing an existing issue.
    """

    class Meta:
        """
        The meta class for the EditForm.
        """
        model = Issue
        fields = ["title", "ai_summary", "description", "category", "email", "assigned_to", "status"]

        # Define the widgets for the form fields.
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control", "placeholder": "Issue title"}),
            "ai_summary": forms.Textarea(attrs={"class": "form-control", "placeholder": "AI summary of the issue"}),
            "category": forms.Select(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "placeholder": "Detailed description of the issue"}),
            "email": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter your email address here"}),
            "assigned_to": forms.Select(attrs={"class": "form-control", "placeholder": "Assigned resource"}),
            "status": forms.Select(attrs={"class": "form-control", "placeholder": "Change issue status"}),
        }
