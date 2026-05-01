from django.urls import path

from . import views

app_name = "advisor"

urlpatterns = [
    path("", views.dashboard_view, name="dashboard"),
    path("result/<int:record_id>/", views.result_view, name="result"),
]
