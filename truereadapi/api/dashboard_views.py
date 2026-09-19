import calendar

from datetime import date, timedelta

from django.db.models import Count, Q
from django.db.models.functions import TruncDate
from django.http import JsonResponse
from rest_framework.decorators import api_view

from .models import (
    MeterReading,
    OcrException,
    Office,
)

# =========================================================
# READING CYCLE
# =========================================================

@api_view(["GET"])
def dashboard_reading_cycle(request):
    filters = get_dashboard_filters(request)

    today = filters["today"]
    billing_month = filters["billing_month"]
    readings = filters["readings"]

    cycle_end = get_month_end(billing_month)

    expected = readings.count()

    total = readings.filter(
        read_at__isnull=False
    ).count()

    # -----------------------------------------------------
    # Current month
    # -----------------------------------------------------

    if billing_month == today.replace(day=1):
        day_of_cycle = today.day
        seven_days_end = today
    else:
        # Historical month = complete cycle
        day_of_cycle = cycle_end.day
        seven_days_end = cycle_end

    # -----------------------------------------------------
    # Last 7 days pace
    # -----------------------------------------------------

    seven_days_start = seven_days_end - timedelta(days=6)

    readings_last_7_days = readings.filter(
        read_at__date__gte=seven_days_start,
        read_at__date__lte=seven_days_end,
    ).count()

    actual_pace = round(
        readings_last_7_days / 7,
        2,
    )

    working_left = max(
        cycle_end.day - day_of_cycle,
        0,
    )

    return JsonResponse({
        "total": total,
        "expected": expected,
        "dayOfCycle": day_of_cycle,
        "cycleDays": cycle_end.day,
        "workingLeft": working_left,
        "actualPace": actual_pace,
    })

# =========================================================
# DASHBOARD ANALYTICS
# =========================================================

@api_view(["GET"])
def dashboard_analytics(request):
    filters = get_dashboard_filters(request)

    today = filters["today"]
    billing_month = filters["billing_month"]
    cycle_readings = filters["readings"]

    cycle_total = cycle_readings.count()

    # =====================================================
    # FUNNEL
    # =====================================================

    ok_total = cycle_readings.filter(
        meter_status__status_code="Ok"
    ).count()

    ocr_clean_total = cycle_readings.filter(
        meter_status__status_code="Ok",
        kwh_ocr_status__status_code="Passed",
    ).count()

    ocr_exception_total = cycle_readings.filter(
        meter_status__status_code="Ok",
        kwh_ocr_status__status_code="Failed",
    ).count()

    defective_total = cycle_readings.filter(
        meter_status__status_code="Defective",
    ).count()

    door_locked_total = cycle_readings.filter(
        meter_status__status_code="Door locked",
    ).count()

    funnel = [
        {
            "key": "total",
            "label": "Total readings",
            "value": cycle_total,
            "parentValue": None,
            "comparisonLabel": "all readings",
            "tone": "good",
            "goodHigh": True,
            "link": "/reports/mr-listconsbill-ocr-ok",
        },
        {
            "key": "ok",
            "label": "OK readings",
            "value": ok_total,
            "parentValue": cycle_total,
            "comparisonLabel": "of total",
            "tone": "good",
            "goodHigh": True,
            "link": "/reports/mr-listconsbill-ocr-ok",
        },
        {
            "key": "ocrClean",
            "label": "OCR clean",
            "value": ocr_clean_total,
            "parentValue": ok_total,
            "comparisonLabel": "of OK",
            "tone": "good",
            "goodHigh": True,
            "link": "/reports/mr-listconsbill-ocr-ok",
        },
        {
            "key": "ocrException",
            "label": "OCR exception",
            "value": ocr_exception_total,
            "parentValue": ok_total,
            "comparisonLabel": "of OK",
            "tone": "bad",
            "goodHigh": False,
            "link": "/reports/mr-listconsbill-ocr-ok",
        },
        {
            "key": "defective",
            "label": "Defective",
            "value": defective_total,
            "parentValue": cycle_total,
            "comparisonLabel": "of total",
            "tone": "bad",
            "goodHigh": False,
            "link": "/reports/mr-listconsbill-ocr-ok",
        },
        {
            "key": "doorLocked",
            "label": "Door locked",
            "value": door_locked_total,
            "parentValue": cycle_total,
            "comparisonLabel": "of total",
            "tone": "good",
            "goodHigh": False,
            "link": "/reports/mr-listconsbill-ocr-ok",
        },
    ]

    # =====================================================
    # DAILY PACE
    # =====================================================

    cycle_end = get_month_end(billing_month)

    if billing_month == today.replace(day=1):
        pace_end_date = today
    else:
        pace_end_date = cycle_end

    cycle_days = cycle_end.day

    expected = cycle_total

    required_per_day = (
        expected / cycle_days
        if cycle_days
        else 0
    )

    daily_rows = (
        cycle_readings
        .filter(
            read_at__isnull=False,
            read_at__date__gte=billing_month,
            read_at__date__lte=pace_end_date,
        )
        .annotate(
            reading_date=TruncDate("read_at")
        )
        .values("reading_date")
        .annotate(
            readings=Count("reading_id")
        )
        .order_by("reading_date")
    )

    daily_map = {
        row["reading_date"]: row["readings"]
        for row in daily_rows
    }

    daily_pace = []

    cumulative = 0

    for day_number in range(
        1,
        pace_end_date.day + 1,
    ):
        current_date = billing_month + timedelta(
            days=day_number - 1
        )

        readings = daily_map.get(
            current_date,
            0,
        )

        cumulative += readings

        required_cumulative = (
            required_per_day * day_number
        )

        daily_pace.append({
            "date": current_date.isoformat(),
            "day": day_number,
            "readings": readings,
            "cumulative": cumulative,
            "requiredPerDay": round(
                required_per_day,
                2,
            ),
            "requiredCumulative": round(
                required_cumulative,
                2,
            ),
        })

    # =====================================================
    # OCR EXCEPTIONS
    # =====================================================

    image_exception_codes = [
        "Image blur",
        "Incorrect Reading",
        "Spoofed Image",
    ]

    parameter_exception_codes = [
        "Parameters Incorrect",
    ]

    image_reading = []

    for exception in (
        OcrException.objects
        .filter(
            exception_code__in=image_exception_codes,
            is_active=True,
        )
        .order_by("ocr_exception_id")
    ):
        count = cycle_readings.filter(
            kwh_ocr_exception_id=exception.ocr_exception_id
        ).count()

        image_reading.append({
            "name": exception.exception_label,
            "value": count,
        })

    parameters = []

    for exception in (
        OcrException.objects
        .filter(
            exception_code__in=parameter_exception_codes,
            is_active=True,
        )
        .order_by("ocr_exception_id")
    ):
        count = cycle_readings.filter(
            kwh_ocr_exception_id=exception.ocr_exception_id
        ).count()

        parameters.append({
            "name": exception.exception_label,
            "value": count,
        })

    # =====================================================
    # SUBDIVISIONS
    # =====================================================

    subdivision_rows = (
        cycle_readings
        .values(
            "office__subdivision_code",
            "office__subdivision_name",
            "office__division_name",
        )
        .annotate(
            readings=Count("reading_id"),
            ok=Count(
                "reading_id",
                filter=Q(
                    meter_status__status_code="Ok"
                ),
            ),
            clean=Count(
                "reading_id",
                filter=Q(
                    meter_status__status_code="Ok",
                    kwh_ocr_status__status_code="Passed",
                ),
            ),
        )
    )

    subdivisions = []

    for row in subdivision_rows:
        readings = row["readings"]
        ok = row["ok"]
        clean = row["clean"]

        clean_rate = (
            (clean / ok) * 100
            if ok
            else 0
        )

        subdivisions.append({
            "name": (
                row["office__subdivision_name"]
                or "Unknown"
            ),
            "division": (
                row["office__division_name"]
                or "Unknown"
            ),
            "readings": readings,
            "ok": ok,
            "clean": round(
                clean_rate,
                2,
            ),
        })

    subdivisions.sort(
        key=lambda item: item["clean"]
    )

    subdivisions = subdivisions[:5]

    # =====================================================
    # FIELD FORCE
    # =====================================================

    month_active_mrs = (
        cycle_readings
        .filter(
            meter_reader_id__isnull=False
        )
        .values(
            "meter_reader_id"
        )
        .distinct()
        .count()
    )

    today_active_mrs = (
        cycle_readings
        .filter(
            read_at__date=today,
            meter_reader_id__isnull=False,
        )
        .values(
            "meter_reader_id"
        )
        .distinct()
        .count()
    )

    # =====================================================
    # AGENCIES
    # =====================================================

    agency_rows = (
        cycle_readings
        .filter(
            agency_id__isnull=False
        )
        .values(
            "agency_id",
            "agency__agency_name",
        )
        .annotate(
            readings=Count("reading_id"),
            ok=Count(
                "reading_id",
                filter=Q(
                    meter_status__status_code="Ok"
                ),
            ),
        )
        .order_by("-readings")
    )

    # Previous month
    previous_month = (
        billing_month - timedelta(days=1)
    ).replace(day=1)

    previous_agency_readings = (
        MeterReading.objects
        .filter(
            billing_month=previous_month,
            agency_id__isnull=False,
        )
    )

    discom = filters["discom"]

    location = filters["location"]

    if discom and discom != "All":
        previous_agency_readings = (
            previous_agency_readings.filter(
                office__discom_name=discom
            )
        )

    if location and location != "All":
        try:
            previous_agency_readings = (
                previous_agency_readings.filter(
                    office_id=int(location)
                )
            )
        except (TypeError, ValueError):
            pass

    previous_agency_rows = (
        previous_agency_readings
        .values("agency_id")
        .annotate(
            readings=Count("reading_id"),
            ok=Count(
                "reading_id",
                filter=Q(
                    meter_status__status_code="Ok"
                ),
            ),
        )
    )

    previous_agency_map = {
        row["agency_id"]: row
        for row in previous_agency_rows
    }

    agencies = []

    for row in agency_rows:
        agency_id = row["agency_id"]

        readings = row["readings"]
        ok = row["ok"]

        ok_rate = (
            (ok / readings) * 100
            if readings
            else 0
        )

        previous = previous_agency_map.get(
            agency_id
        )

        if previous and previous["readings"]:
            previous_ok_rate = (
                previous["ok"]
                / previous["readings"]
                * 100
            )

            trend = (
                ok_rate
                - previous_ok_rate
            )
        else:
            trend = 0

        agencies.append({
            "name": (
                row["agency__agency_name"]
                or "Unknown"
            ),
            "readings": readings,
            "ok": round(
                ok_rate,
                2,
            ),
            "trend": round(
                trend,
                2,
            ),
        })

    return JsonResponse({
        "exceptions": {
            "okTotal": ok_total,
            "imageReading": image_reading,
            "parameters": parameters,
        },

        "subdivisions": subdivisions,

        "fieldForce": {
            "activeMonth": month_active_mrs,
            "activeToday": today_active_mrs,
            "agencies": agencies,
        },

        "cycle": {
            "total": cycle_total,
            "expected": expected,
            "cycleDays": cycle_days,
            "dailyPace": daily_pace,
        },

        "funnel": funnel,
    })


@api_view(["GET"])
def dashboard_month_on_month(request):
    filters = get_dashboard_filters(request)

    selected_month = filters["billing_month"]

    months = []

    month_cursor = selected_month

    for _ in range(7):
        billing_month = month_cursor

        readings = MeterReading.objects.filter(
            billing_month=billing_month
        )

        # Apply selected discom
        discom = filters["discom"]

        if discom and discom != "All":
            readings = readings.filter(
                office__discom_name=discom
            )

        # Apply selected location
        location = filters["location"]

        if location and location != "All":
            try:
                readings = readings.filter(
                    office_id=int(location)
                )
            except (TypeError, ValueError):
                pass

        total = readings.count()

        proper_reading = readings.filter(
            meter_status__status_code="Ok"
        ).count()

        without_exception_passed = readings.filter(
            kwh_ocr_status__status_code="Passed"
        ).count()

        def exception_count(code):
            return readings.filter(
                kwh_ocr_exception__exception_code=code
            ).count()

        image_blur = exception_count(
            "Image blur"
        )

        image_spoofed = exception_count(
            "Spoofed Image"
        )

        meter_dirty = exception_count(
            "Meter Dirty"
        )

        incorrect_reading = exception_count(
            "Incorrect Reading"
        )

        parameters_mismatch = exception_count(
            "Parameters Incorrect"
        )

        parameters_unavailable = 0
        unclassified = 0

        months.append({
            "month": billing_month.strftime(
                "%b %Y"
            ),
            "totalReadings": total,
            "properReading": proper_reading,
            "withoutExceptionPassed": (
                without_exception_passed
            ),
            "imageBlur": image_blur,
            "imageSpoofed": image_spoofed,
            "meterDirty": meter_dirty,
            "incorrectReading": incorrect_reading,
            "parametersUnavailable": (
                parameters_unavailable
            ),
            "parametersMismatch": (
                parameters_mismatch
            ),
            "unclassified": unclassified,
        })

        month_cursor = (
            billing_month
            - timedelta(days=1)
        ).replace(day=1)

    months.reverse()

    return JsonResponse({
        "months": months
    })

# =========================================================
# NEEDS ATTENTION
# =========================================================

@api_view(["GET"])
def dashboard_needs_attention(request):
    filters = get_dashboard_filters(request)

    billing_month = filters["billing_month"]
    readings = filters["readings"]

    def exception_count(code):
        return readings.filter(
            kwh_ocr_exception__exception_code=code
        ).count()

    incorrect_reading = exception_count(
        "Incorrect Reading"
    )

    spoofed_image = exception_count(
        "Spoofed Image"
    )

    image_blur = exception_count(
        "Image blur"
    )

    parameter_issues = exception_count(
        "Parameters Incorrect"
    )

    items = [
        {
            "value": f"{incorrect_reading:,}",
            "title": "Incorrect readings",
            "description": (
                "Readings flagged as incorrect "
                "by OCR validation."
            ),
            "type": "red",
            "link": "/dashboard/incorrect-readings",
        },
        {
            "value": f"{spoofed_image:,}",
            "title": "Spoofed images",
            "description": (
                "Images flagged as potentially "
                "spoofed during validation."
            ),
            "type": "red",
            "link": "/dashboard/spoofed-images",
        },
        {
            "value": f"{image_blur:,}",
            "title": "Image blur",
            "description": (
                "Readings affected by image "
                "quality or blur."
            ),
            "type": "amber",
            "link": "/dashboard/image-blur",
        },
        {
            "value": f"{parameter_issues:,}",
            "title": "Parameter issues",
            "description": (
                "Readings with parameter-related "
                "OCR exceptions."
            ),
            "type": "violet",
            "link": "/dashboard/parameter-issues",
        },
    ]

    return JsonResponse({
        "items": items,
        "billingMonth": billing_month.isoformat(),
    })

# =========================================================
# DASHBOARD FILTER HELPERS
# =========================================================

def get_dashboard_filters(request):
    """
    Read dashboard filters from query parameters.

    Supported:
        month=YYYY-MM-01
        discom=SBPDCL
        location=office_id
    """

    today = date.today()

    month_param = request.GET.get("month")
    discom = request.GET.get("discom")
    location = request.GET.get("location")

    # -----------------------------------------------------
    # Month
    # -----------------------------------------------------

    if month_param:
        try:
            billing_month = date.fromisoformat(month_param)
            billing_month = billing_month.replace(day=1)
        except ValueError:
            billing_month = today.replace(day=1)
    else:
        billing_month = today.replace(day=1)

    # -----------------------------------------------------
    # Base queryset
    # -----------------------------------------------------

    readings = MeterReading.objects.filter(
        billing_month=billing_month
    )

    # -----------------------------------------------------
    # Discom
    # -----------------------------------------------------

    if discom and discom != "All":
        readings = readings.filter(
            office__discom_name=discom
        )

    # -----------------------------------------------------
    # Location
    #
    # Location is represented by office_id from the
    # secondary navigation.
    # -----------------------------------------------------

    if location and location != "All":
        try:
            location_id = int(location)

            readings = readings.filter(
                office_id=location_id
            )
        except (TypeError, ValueError):
            pass

    return {
        "today": today,
        "billing_month": billing_month,
        "readings": readings,
        "discom": discom,
        "location": location,
    }


def get_month_end(billing_month):
    """Return the last day of a billing month."""

    last_day = calendar.monthrange(
        billing_month.year,
        billing_month.month,
    )[1]

    return billing_month.replace(day=last_day)

# =========================================================
# DASHBOARD FILTERS
# =========================================================

@api_view(["GET"])
def dashboard_filters(request):
    """
    Return filter options for the dashboard
    secondary navigation.
    """

    today = date.today()

    # -----------------------------------------------------
    # Months
    # -----------------------------------------------------

    month_rows = (
        MeterReading.objects
        .values("billing_month")
        .annotate(
            readings=Count("reading_id")
        )
        .order_by("-billing_month")
    )

    months = [
        {
            "value": row["billing_month"].isoformat(),
            "label": row["billing_month"].strftime(
                "%B %Y"
            ),
        }
        for row in month_rows
        if row["billing_month"]
    ]

    # -----------------------------------------------------
    # Discoms
    # -----------------------------------------------------

    discom_rows = (
        Office.objects
        .exclude(discom_name__isnull=True)
        .exclude(discom_name="")
        .values_list(
            "discom_name",
            flat=True,
        )
        .distinct()
        .order_by("discom_name")
    )

    discoms = list(discom_rows)

    # -----------------------------------------------------
    # Locations
    # -----------------------------------------------------

    location_rows = (
        Office.objects
        .exclude(section_name__isnull=True)
        .exclude(section_name="")
        .values(
            "office_id",
            "zone_name",
            "circle_name",
            "division_name",
            "subdivision_name",
            "section_name",
        )
        .order_by(
            "zone_name",
            "circle_name",
            "division_name",
            "subdivision_name",
            "section_name",
        )
    )

    locations = []

    for row in location_rows:
        locations.append({
            "id": row["office_id"],
            "zone": row["zone_name"],
            "circle": row["circle_name"],
            "division": row["division_name"],
            "subdivision": row["subdivision_name"],
            "section": row["section_name"],
            "label": (
                row["section_name"]
                or row["subdivision_name"]
                or row["division_name"]
                or row["circle_name"]
                or row["zone_name"]
                or "Unknown"
            ),
        })

    # -----------------------------------------------------
    # Defaults
    # -----------------------------------------------------

    current_month = today.replace(day=1)

    available_month_values = {
        item["value"]
        for item in months
    }

    if current_month.isoformat() in available_month_values:
        default_month = current_month.isoformat()
    elif months:
        default_month = months[0]["value"]
    else:
        default_month = None

    # Keep current behaviour of showing SBPDCL when it
    # exists, otherwise use All.
    if "SBPDCL" in discoms:
        default_discom = "SBPDCL"
    elif len(discoms) == 1:
        default_discom = discoms[0]
    else:
        default_discom = "All"

    return JsonResponse({
        "months": months,
        "discoms": discoms,
        "locations": locations,
        "defaults": {
            "month": default_month,
            "discom": default_discom,
            "location": "All",
        },
    })