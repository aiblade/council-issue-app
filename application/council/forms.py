from django import forms
from .models import Issue


class IssueForm(forms.ModelForm):
    class Meta:
        model = Issue
        fields = ["title", "description", "category", "email"]

        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control", "placeholder": "Issue title"}),
            "category": forms.Select(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "placeholder": "Detailed description of the issue"}),
            "email": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter your email address here"})
        }

class EditForm(forms.ModelForm):
    class Meta:
        model = Issue
        fields = ["title", "ai_summary", "description", "category", "email", "assigned_to", "status"]

        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control", "placeholder": "Issue title"}),
            "ai_summary": forms.Textarea(attrs={"class": "form-control", "placeholder": "AI summary of the issue"}),
            "category": forms.Select(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "placeholder": "Detailed description of the issue"}),
            "email": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter your email address here"}),
            "assigned_to": forms.Select(attrs={"class": "form-control", "placeholder": "Assigned resource"}),
            "status": forms.Select(attrs={"class": "form-control", "placeholder": "Change issue status"}),
        }