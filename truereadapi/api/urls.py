from django.urls import path
from . import dashboard_views
from . import notification_views
from .viewsfolder import consumer_profile_views

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

    # Notifications
    path(
        "notificationdatagrid/",
        notification_views.notification_datagrid,
        name="notification-datagrid",
    ),
    path(
        "discom/",
        notification_views.notification_discom,
        name="notification-discom",
    ),
    path(
        "zone/",
        notification_views.notification_zone,
        name="notification-zone",
    ),
    path(
        "circle/",
        notification_views.notification_circle,
        name="notification-circle",
    ),
    path(
        "division/",
        notification_views.notification_division,
        name="notification-division",
    ),
    path(
        "subdivision/",
        notification_views.notification_subdivision,
        name="notification-subdivision",
    ),
    path(
        "section/",
        notification_views.notification_section,
        name="notification-section",
    ),
    path(
        "savenotification/",
        notification_views.save_notification,
        name="save-notification",
    ),

    # Consumer Profile
    path(
        "reports/consumer-profile/<str:consumer_account_no>/",
        consumer_profile_views.consumer_profile,
        name="consumer-profile",
    ),
]