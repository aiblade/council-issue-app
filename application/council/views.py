from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Issue
from .forms import IssueForm, EditForm
from django.urls import reverse_lazy


class IssuesView(ListView):
    model = Issue
    template_name = "home.html"
    ordering = ["-id"]

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

class DeleteIssueView(DeleteView):
    model = Issue
    template_name = "delete_issue.html"
    success_url = reverse_lazy("home")