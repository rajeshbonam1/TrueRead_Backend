from decimal import Decimal

from django.db.models import Count, Q
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from ..models import MeterReading


def decimal_to_number(value):
    """
    Convert Decimal values into JSON-friendly numbers.
    """
    if value is None:
        return None

    if isinstance(value, Decimal):
        return float(value)

    return value


def serialize_date(value):
    if value is None:
        return None

    return value.isoformat()


def get_consumption(current_reading, previous_reading):
    """
    Consumption = current KWH reading - previous KWH reading.

    Uses kwh_reading as the primary reading.
    Falls back to kwh_ocr_reading when kwh_reading is unavailable.
    """

    current_value = (
        current_reading.kwh_reading
        if current_reading.kwh_reading is not None
        else current_reading.kwh_ocr_reading
    )

    if current_value is None:
        return None

    previous_value = None

    if previous_reading:
        previous_value = (
            previous_reading.kwh_reading
            if previous_reading.kwh_reading is not None
            else previous_reading.kwh_ocr_reading
        )

    if previous_value is None:
        return None

    return current_value - previous_value


def get_reading_value(reading):
    if reading.kwh_reading is not None:
        return decimal_to_number(reading.kwh_reading)

    if reading.kwh_ocr_reading is not None:
        return decimal_to_number(reading.kwh_ocr_reading)

    return None


def get_exception_label(reading):
    """
    Return the most relevant exception/abnormality label.
    """

    if reading.abnormality:
        return reading.abnormality.abnormality_label

    if reading.kwh_ocr_exception:
        return reading.kwh_ocr_exception.exception_label

    if reading.kwh_img_check:
        return reading.kwh_img_check.check_label

    if reading.meter_status:
        status_label = reading.meter_status.status_label

        if status_label.lower() not in {
            "active",
            "normal",
            "ok",
        }:
            return status_label

    return None


def get_reading_status(reading):
    """
    Determine the UI status for a reading.
    """

    exception = get_exception_label(reading)

    if exception:
        return {
            "status": "exception",
            "label": exception,
        }

    return {
        "status": "ok",
        "label": "No Exception Found",
    }


def build_consumer_profile(readings):
    """
    Build the complete consumer profile response from
    the consumer's meter readings.
    """

    latest = readings[0]

    office = latest.office
    agency = latest.agency
    meter_reader = latest.meter_reader

    # ----------------------------------------------------------
    # Recent readings / consumption
    # ----------------------------------------------------------

    recent_source = list(readings[:12])

    recent_readings = []

    for index, reading in enumerate(recent_source):
        previous = (
            recent_source[index + 1]
            if index + 1 < len(recent_source)
            else None
        )

        consumption = get_consumption(
            reading,
            previous,
        )

        status_info = get_reading_status(reading)

        recent_readings.append({
            "reading_id": reading.reading_id,
            "billing_month": serialize_date(
                reading.billing_month
            ),
            "month": reading.billing_month.strftime("%b %Y"),
            "read_at": serialize_date(reading.read_at),
            "reading": get_reading_value(reading),
            "consumption": decimal_to_number(consumption),
            "reader_name": (
                meter_reader.reader_name
                if meter_reader
                else None
            ),
            "status": status_info["status"],
            "status_label": status_info["label"],
            "image_key": reading.kwh_img_key,
            "remark": reading.reader_remark,
        })

    # ----------------------------------------------------------
    # Consumption trend
    # ----------------------------------------------------------

    trend = []

    # Reverse so oldest → newest for the chart.
    chronological = list(reversed(recent_source))

    for index, reading in enumerate(chronological):
        previous = (
            chronological[index - 1]
            if index > 0
            else None
        )

        consumption = get_consumption(
            reading,
            previous,
        )

        trend.append({
            "month": reading.billing_month.strftime("%b"),
            "billing_month": serialize_date(
                reading.billing_month
            ),
            "consumption": decimal_to_number(
                consumption
            ),
        })

    # ----------------------------------------------------------
    # Latest / previous consumption
    # ----------------------------------------------------------

    latest_consumption = None

    if len(recent_source) > 1:
        latest_consumption = get_consumption(
            recent_source[0],
            recent_source[1],
        )

    # ----------------------------------------------------------
    # 12-month average
    # ----------------------------------------------------------

    valid_consumptions = [
        item["consumption"]
        for item in trend
        if item["consumption"] is not None
    ]

    average_12_months = None

    if valid_consumptions:
        average_12_months = (
            sum(valid_consumptions)
            / len(valid_consumptions)
        )

    # ----------------------------------------------------------
    # Exception count
    # ----------------------------------------------------------

    exception_readings = [
        reading
        for reading in recent_source
        if get_exception_label(reading)
    ]

    # ----------------------------------------------------------
    # Read success
    #
    # For the available data, successful reads are readings
    # without an exception. The UI can display X/12.
    # ----------------------------------------------------------

    total_months = min(len(recent_source), 12)

    successful_reads = sum(
        1
        for reading in recent_source
        if not get_exception_label(reading)
    )

    # ----------------------------------------------------------
    # Consumer
    # ----------------------------------------------------------

    consumer = {
        "account_no": latest.consumer_account_no,
        "name": latest.consumer_name,
        "status": "Active",
        "tariff_category": latest.tariff_category,
        "load": None,
        "phase": (
            latest.meter_phase.phase_label
            if latest.meter_phase
            else None
        ),
        "address": None,
        "meter_serial_no": latest.meter_serial_no,
        "installed_on": None,
        "agency": (
            agency.agency_name
            if agency
            else (
                office.agency_name
                if office
                else None
            )
        ),
    }

    # ----------------------------------------------------------
    # Summary cards
    # ----------------------------------------------------------

    summary = {
        "latest_reading": get_reading_value(latest),
        "latest_reading_date": serialize_date(
            latest.read_at
        ),
        "last_consumption": decimal_to_number(
            latest_consumption
        ),
        "consumption_change_percent": None,
        "average_12_months": (
            round(average_12_months, 2)
            if average_12_months is not None
            else None
        ),
        "valid_read_months": len(valid_consumptions),
        "read_success": (
            f"{successful_reads}/{total_months}"
            if total_months
            else "0/0"
        ),
        "months_with_exception": len(
            exception_readings
        ),
    }

    # ----------------------------------------------------------
    # Meter details
    # ----------------------------------------------------------

    meter = {
        "serial_no": latest.meter_serial_no,
        "make_model": None,
        "type": latest.meter_type,
        "phase": (
            latest.meter_phase.phase_label
            if latest.meter_phase
            else None
        ),
        "multiplying_factor": decimal_to_number(
            latest.meter_multiplication_factor
        ),
        "installed_on": None,
        "last_replaced": None,
        "status": (
            latest.meter_status.status_label
            if latest.meter_status
            else None
        ),
    }

    # ----------------------------------------------------------
    # Location
    # ----------------------------------------------------------

    location = {
        "discom": (
            office.discom_name
            if office
            else None
        ),
        "zone": (
            office.zone_name
            if office
            else None
        ),
        "circle": (
            office.circle_name
            if office
            else None
        ),
        "division": (
            office.division_name
            if office
            else None
        ),
        "subdivision": (
            office.subdivision_name
            if office
            else None
        ),
        "section": (
            office.section_name
            if office
            else None
        ),
        "section_code": (
            office.section_code
            if office
            else None
        ),
    }

    # ----------------------------------------------------------
    # Assigned meter reader
    # ----------------------------------------------------------

    assigned_meter_reader = None

    if meter_reader:
        assigned_meter_reader = {
            "id": meter_reader.meter_reader_id,
            "reader_code": meter_reader.reader_code,
            "name": meter_reader.reader_name,
            "phone": meter_reader.phone_no,
            "agency": (
                agency.agency_name
                if agency
                else (
                    office.agency_name
                    if office
                    else None
                )
            ),
            "reads_this_cycle": None,
            "last_visit": serialize_date(
                latest.read_at
            ),
        }

    # ----------------------------------------------------------
    # Exceptions
    # ----------------------------------------------------------

    exception_counts = {}

    for reading in recent_source:
        exception_label = get_exception_label(reading)

        if exception_label:
            exception_counts[exception_label] = (
                exception_counts.get(
                    exception_label,
                    0,
                )
                + 1
            )

    exceptions = [
        {
            "name": name,
            "count": count,
        }
        for name, count in exception_counts.items()
    ]

    # Clean readings for API response
    return {
        "consumer": consumer,
        "summary": summary,
        "consumption_trend": trend,
        "recent_readings": recent_readings[:4],
        "meter": meter,
        "location": location,
        "meter_reader": assigned_meter_reader,
        "exceptions": exceptions,
    }


@api_view(["GET"])
def consumer_profile(request, consumer_account_no):
    """
    Consumer Profile API.

    Example:
        GET /reports/consumer-profile/239100391/
    """

    readings = (
        MeterReading.objects
        .filter(
            consumer_account_no=consumer_account_no
        )
        .select_related(
            "office",
            "agency",
            "meter_reader",
            "meter_phase",
            "meter_status",
            "kwh_ocr_status",
            "kwh_ocr_exception",
            "kwh_img_check",
            "abnormality",
        )
        .order_by(
            "-billing_month",
            "-read_at",
        )
    )

    if not readings.exists():
        return Response(
            {
                "error": "Consumer not found",
                "consumer_account_no": (
                    consumer_account_no
                ),
            },
            status=status.HTTP_404_NOT_FOUND,
        )

    data = build_consumer_profile(
        list(readings)
    )

    return Response(data)