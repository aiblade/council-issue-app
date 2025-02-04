from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView
from .models import Issue


class IssuesView(ListView):
    model = Issue
    template_name = "issues.html"
    context_object_name = "issues"


class IssueDetailView(DetailView):
    model = Issue
    template_name = "issue_details.html"
    
class CreateIssueView(CreateView):
    model = Issue
    template_name = "create_issue.html"
    fields = ["title", "description", "category", "email"]