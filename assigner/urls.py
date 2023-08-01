from django.urls import path
from assigner.api.viewsets.accounts import (
    AccountsCreateViewSet,
    LoginViewSet,
    ProjectCreateViewSet,
    ProjectListViewSet,
    ProjectEditViewSet,
    TaskCreateViewSet,
    TaskEditViewSet,
    TaskListViewSet,
    SubmitTaskViewSet,
    SubmitTaskEditViewSet,
    TaskSubmitListViewSet,
)


urlpatterns = [
    path("account-registration/", AccountsCreateViewSet.as_view()),
    path("login/", LoginViewSet.as_view()),
    path("project-create/", ProjectCreateViewSet.as_view()),
    path("project-list/", ProjectListViewSet.as_view()),
    path("project-edit/<str:pk>/", ProjectEditViewSet.as_view()),
    path("task-create/", TaskCreateViewSet.as_view()),
    path("task-edit/<str:pk>/", TaskEditViewSet.as_view()),
    path("task-list/", TaskListViewSet.as_view()),
    path("task-submitting-create/", SubmitTaskViewSet.as_view()),
    path("task-submitted-edit/<str:pk>/", SubmitTaskEditViewSet.as_view()),
    path("task-submitted-list/", TaskSubmitListViewSet.as_view()),
]
