from django.urls import path
from .views import IssuesView, IssueDetailView

urlpatterns = [
    path("", IssuesView.as_view(), name="home"),
    path("issue/<int:pk>", IssueDetailView.as_view(), name="issue-detail"),
]
