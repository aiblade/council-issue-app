from django.urls import path
from .views import IssuesView, IssueDetailView, CreateIssueView

urlpatterns = [
    path("", IssuesView.as_view(), name="home"),
    path("issue/<int:pk>", IssueDetailView.as_view(), name="issue-detail"),
    path("create_issue/", CreateIssueView.as_view(), name="create-issue"),
]
