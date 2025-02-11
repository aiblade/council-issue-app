from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Issue
from .forms import IssueForm, EditForm
from django.urls import reverse_lazy
from aisummary.utils import generate_ai_summary_async


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

    def form_valid(self, form):
        """
        If the form is valid, generate the AI summary asynchronously and return the response.
        :param form: The form instance.
        :return: The response.
        """

        # Call the parent form_valid method to save the form data.
        response = super().form_valid(form)
        generate_ai_summary_async(self.object.id)
        return response


class UpdateIssueView(UpdateView):
    model = Issue
    form_class = EditForm
    template_name = "update_issue.html"


class DeleteIssueView(DeleteView):
    model = Issue
    template_name = "delete_issue.html"
    success_url = reverse_lazy("home")