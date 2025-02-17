from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Issue
from .forms import IssueForm, EditForm
from django.urls import reverse_lazy
from aisummary.utils import generate_ai_summary_async


class IssuesView(ListView):
    """
    The view for the home page, which displays a list of all issues.
    """

    model = Issue
    template_name = "home.html"
    ordering = ["-id"]


class IssueDetailView(DetailView):
    """
    The view for displaying the details of a single issue.
    """

    model = Issue
    template_name = "issue_details.html"


class CreateIssueView(CreateView):
    """
    The view for creating a new issue.
    """

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
    """
    The view for updating an existing issue.
    """

    model = Issue
    form_class = EditForm
    template_name = "update_issue.html"


class DeleteIssueView(DeleteView):
    """
    The view for deleting an existing issue.
    """

    model = Issue
    template_name = "delete_issue.html"
    success_url = reverse_lazy("home")