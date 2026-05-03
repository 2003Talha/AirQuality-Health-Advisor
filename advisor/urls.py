from django.urls import path

from . import views

app_name = "advisor"

urlpatterns = [
    path("", views.dashboard_view, name="dashboard"),
    path("result/<int:record_id>/", views.result_view, name="result"),
    path("history/", views.history_view, name="history"),
    path("check-model-status/", views.check_model_status_view, name="check_model_status"),
]
