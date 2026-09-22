from django.db import transaction
from django.utils import timezone
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import (
    Agency,
    MeterReader,
    NotificationMani,
    NotificationRecipients,
    Office,
)


# ----------------------------------------------------------------------
# Helpers
# ----------------------------------------------------------------------

LOCATION_FIELDS = {
    "discom": "discom_name",
    "zone": "zone_name",
    "circle": "circle_name",
    "division": "division_name",
    "subdivision": "subdivision_name",
    "sectioncode": "section_code",
}


def get_location_offices(locationwise, locationname):
    """
    Return offices matching the notification location.

    Example:
        locationwise = "zone"
        locationname = "SOUTH BIHAR RURAL"
    """

    field_name = LOCATION_FIELDS.get(locationwise)

    if not field_name:
        return Office.objects.none()

    return Office.objects.filter(
        **{field_name: locationname}
    )


def get_recipients_for_location(locationwise, locationname):
    """
    Return meter readers belonging to the selected offices.
    """

    offices = get_location_offices(
        locationwise,
        locationname,
    )

    return MeterReader.objects.filter(
        office__in=offices
    ).select_related("office", "office__agency")


def get_recipients_for_agency(agency_name):
    """
    Return meter readers belonging to offices associated
    with the requested agency name.
    """

    offices = Office.objects.filter(
        agency__agency_name=agency_name
    )

    return MeterReader.objects.filter(
        office__in=offices
    ).select_related("office", "office__agency")


def create_notification_recipients(notification, meter_readers):
    """
    Create notification recipient records for the selected
    meter readers.

    Firebase tokens are intentionally left empty because the
    current meter_reader table does not contain a token field.
    """

    recipients = []

    for meter_reader in meter_readers:
        office = meter_reader.office

        recipients.append(
            NotificationRecipients(
                notification_id=notification,
                mr_id=meter_reader.reader_code,
                mr_name=meter_reader.reader_name,
                mr_token_id="",
                mr_mobile_number=meter_reader.phone_no,
                mr_location_section_id=(
                    office.section_code if office else ""
                ),
                message_image_url=notification.message_image_url,
                message_delivery_status="pending",
                message_title=notification.message_title,
                message_content=notification.message_content,
                mr_agency=(
                    office.agency.agency_name
                    if office and office.agency
                    else ""
                ),
            )
        )

    if recipients:
        NotificationRecipients.objects.bulk_create(
            recipients
        )

    return len(recipients)


# ----------------------------------------------------------------------
# Notification Datagrid
# ----------------------------------------------------------------------

@api_view(["GET"])
def notification_datagrid(request):
    """
    Return all notifications for the notification data grid.
    """

    notifications = (
        NotificationMani.objects
        .all()
        .order_by("-id")
    )

    data = []

    for notification in notifications:
        data.append({
            "id": notification.id,
            "message_type": notification.message_type,
            "notification_criteria": notification.notification_criteria,
            "location_id": notification.location_id,
            "locationname": notification.location_id,
            "notification_status": notification.notification_status,
            "message_image_url": notification.message_image_url,
            "message_title": notification.message_title,
            "message_content": notification.message_content,
            "message_schedule_type": notification.message_schedule_type,
            "Message_delivery_date_time": (
                notification.Message_delivery_date_time
            ),
            "message_delivery_date_time": (
                notification.Message_delivery_date_time
            ),
            "scheduled_time": notification.scheduled_time,
            "message_scheduled_time": notification.scheduled_time,
        })

    return Response(data)


# ----------------------------------------------------------------------
# Discom
# ----------------------------------------------------------------------

@api_view(["GET"])
def notification_discom(request):
    """
    Return available DISCOM names.
    """

    values = (
        Office.objects
        .values_list("discom_name", flat=True)
        .distinct()
        .order_by("discom_name")
    )

    return Response([
        value
        for value in values
        if value
    ])


# ----------------------------------------------------------------------
# Zone
# ----------------------------------------------------------------------

@api_view(["POST"])
def notification_zone(request):
    discom = request.data.get("discom")

    if not discom:
        return Response(
            {"error": "discom is required"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    values = (
        Office.objects
        .filter(discom_name=discom)
        .values_list("zone_name", flat=True)
        .distinct()
        .order_by("zone_name")
    )

    return Response([
        value
        for value in values
        if value
    ])


# ----------------------------------------------------------------------
# Circle
# ----------------------------------------------------------------------

@api_view(["POST"])
def notification_circle(request):
    zone = request.data.get("zone")

    if not zone:
        return Response(
            {"error": "zone is required"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    values = (
        Office.objects
        .filter(zone_name=zone)
        .values_list("circle_name", flat=True)
        .distinct()
        .order_by("circle_name")
    )

    return Response([
        value
        for value in values
        if value
    ])


# ----------------------------------------------------------------------
# Division
# ----------------------------------------------------------------------

@api_view(["POST"])
def notification_division(request):
    circle = request.data.get("circle")

    if not circle:
        return Response(
            {"error": "circle is required"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    values = (
        Office.objects
        .filter(circle_name=circle)
        .values_list("division_name", flat=True)
        .distinct()
        .order_by("division_name")
    )

    return Response([
        value
        for value in values
        if value
    ])


# ----------------------------------------------------------------------
# Subdivision
# ----------------------------------------------------------------------

@api_view(["POST"])
def notification_subdivision(request):
    division = request.data.get("division")

    if not division:
        return Response(
            {"error": "division is required"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    values = (
        Office.objects
        .filter(division_name=division)
        .values_list("subdivision_name", flat=True)
        .distinct()
        .order_by("subdivision_name")
    )

    return Response([
        value
        for value in values
        if value
    ])


# ----------------------------------------------------------------------
# Section
# ----------------------------------------------------------------------

@api_view(["POST"])
def notification_section(request):
    subdivision = request.data.get("subdivision")

    if not subdivision:
        return Response(
            {"error": "subdivision is required"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    values = (
        Office.objects
        .filter(subdivision_name=subdivision)
        .values_list(
            "section_code",
            flat=True,
        )
        .distinct()
        .order_by("section_code")
    )

    return Response([
        value
        for value in values
        if value
    ])


# ----------------------------------------------------------------------
# Save Templated Notification
# ----------------------------------------------------------------------

@api_view(["POST"])
def save_notification(request):
    """
    Create a templated notification and its recipients.
    """

    data = request.data

    message_type = data.get("message_type")
    notification_criteria = data.get("notification_criteria")
    locationwise = data.get("locationwise")
    locationname = data.get("locationname")

    notification_status = data.get(
        "notification_status",
        "active",
    )

    message_schedule_type = data.get(
        "message_schedule_type",
        "now",
    )

    message_title = data.get("message_title")
    message_content = data.get("message_content")
    scheduled_time = data.get("scheduled_time")
    message_image_url = data.get(
        "message_image_url",
        "",
    )

    if not message_type:
        return Response(
            {"error": "message_type is required"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if not notification_criteria:
        return Response(
            {"error": "notification_criteria is required"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if not locationwise:
        return Response(
            {"error": "locationwise is required"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if not locationname:
        return Response(
            {"error": "locationname is required"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if notification_criteria == "Location":
        meter_readers = get_recipients_for_location(
            locationwise,
            locationname,
        )

    elif notification_criteria == "Agency":
        meter_readers = get_recipients_for_agency(
            locationname,
        )

    else:
        return Response(
            {
                "error": (
                    "notification_criteria must be "
                    "'Location' or 'Agency'"
                )
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    meter_readers = list(meter_readers)

    if not meter_readers:
        return Response(
            {
                "error": "No meter readers found",
                "recipient_count": 0,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    location_id = f"{locationwise}/{locationname}"

    with transaction.atomic():
        notification = NotificationMani.objects.create(
            message_type=message_type,
            notification_criteria=notification_criteria,
            location_id=location_id,
            notification_status=notification_status,
            message_image_url=message_image_url,
            message_title=message_title,
            message_content=message_content,
            message_schedule_type=message_schedule_type,
            Message_delivery_date_time=timezone.now(),
            scheduled_time=scheduled_time,
        )

        recipient_count = create_notification_recipients(
            notification,
            meter_readers,
        )

    return Response(
        {
            "message": "Notification saved successfully",
            "notification_id": notification.id,
            "recipient_count": recipient_count,
        },
        status=status.HTTP_201_CREATED,
    )