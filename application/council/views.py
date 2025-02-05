from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from .models import Issue
from .forms import IssueForm, EditForm


class IssuesView(ListView):
    model = Issue
    template_name = "issues.html"
    context_object_name = "issues"


class IssueDetailView(DetailView):
    model = Issue
    template_name = "issue_details.html"
    
class CreateIssueView(CreateView):
    model = Issue
    form_class = IssueForm
    template_name = "create_issue.html"

class UpdateIssueView(UpdateView):
    model = Issue
    form_class = EditForm
    template_name = "update_issue.html"