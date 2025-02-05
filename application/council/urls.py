from django.urls import path
from .views import IssuesView, IssueDetailView, CreateIssueView, UpdateIssueView, DeleteIssueView

urlpatterns = [
    path("", IssuesView.as_view(), name="home"),
    path("issue/<int:pk>", IssueDetailView.as_view(), name="issue-detail"),
    path("create_issue/", CreateIssueView.as_view(), name="create-issue"),
    path("issue/edit/<int:pk>", UpdateIssueView.as_view(), name="update-issue"),
    path("issue/delete/<int:pk>", DeleteIssueView.as_view(), name="delete-issue"),
]
