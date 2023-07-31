from django.urls import path
from assigner.api.viewsets.accounts import AccountsCreateViewSet


urlpatterns = [
    path("account-registration/", AccountsCreateViewSet.as_view()),
]
