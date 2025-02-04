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