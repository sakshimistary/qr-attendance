from django.urls import path

from classes.views import AttendanceView

urlpatterns = [
    path("attendance", AttendanceView.as_view(), name="attendance"),
]
