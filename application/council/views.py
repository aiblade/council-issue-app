from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Issue


class IssuesView(ListView):
    model = Issue
    template_name = "issues.html"
    context_object_name = "issues"


class IssueDetailView(DetailView):
    model = Issue
    template_name = "issue_details.html"
    
