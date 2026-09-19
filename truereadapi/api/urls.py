from django.urls import path
from . import dashboard_views

urlpatterns = [
    path(
        "dashboard/reading-cycle/",
        dashboard_views.dashboard_reading_cycle,
        name="dashboard-reading-cycle",
    ),
    path(
        "dashboard/analytics/",
        dashboard_views.dashboard_analytics,
        name="dashboard-analytics",
    ),
    path(
        "dashboard/month-on-month/",
        dashboard_views.dashboard_month_on_month,
        name="dashboard-month-on-month",
    ),
    path(
        "dashboard/needs-attention/",
        dashboard_views.dashboard_needs_attention,
        name="dashboard-needs-attention",
    ),
    path(
        "dashboard/filters/",
    dashboard_views.dashboard_filters,
    name="dashboard-filters",
    ),
]