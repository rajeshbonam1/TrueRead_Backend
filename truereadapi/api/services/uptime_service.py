# services/uptime_service.py
import boto3
from datetime import datetime, timedelta, timezone

cloudwatch = boto3.client("cloudwatch", region_name="us-east-1")

def get_lambda_uptime(function_name):
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(days=30)

    response = cloudwatch.get_metric_statistics(
        Namespace="AWS/Lambda",
        MetricName="Invocations",
        Dimensions=[{"Name": "FunctionName", "Value": function_name}],
        StartTime=start_time,
        EndTime=end_time,
        Period=86400,
        Statistics=["Sum"]
    )

    error_response = cloudwatch.get_metric_statistics(
        Namespace="AWS/Lambda",
        MetricName="Errors",
        Dimensions=[{"Name": "FunctionName", "Value": function_name}],
        StartTime=start_time,
        EndTime=end_time,
        Period=86400,
        Statistics=["Sum"]
    )

    total_invocations = sum(dp["Sum"] for dp in response["Datapoints"])
    total_errors = sum(dp["Sum"] for dp in error_response["Datapoints"])

    if total_invocations == 0:
        return 100.0

    uptime = ((total_invocations - total_errors) / total_invocations) * 100
    return round(uptime, 2)

def get_lambda_uptime_by_range(function_name, start_time, end_time):
    """
    Calculate lambda uptime for a given date range
    """

    response = cloudwatch.get_metric_statistics(
        Namespace="AWS/Lambda",
        MetricName="Invocations",
        Dimensions=[{"Name": "FunctionName", "Value": function_name}],
        StartTime=start_time,
        EndTime=end_time,
        Period=86400,  # 1 day
        Statistics=["Sum"]
    )

    error_response = cloudwatch.get_metric_statistics(
        Namespace="AWS/Lambda",
        MetricName="Errors",
        Dimensions=[{"Name": "FunctionName", "Value": function_name}],
        StartTime=start_time,
        EndTime=end_time,
        Period=86400,
        Statistics=["Sum"]
    )

    total_invocations = sum(dp["Sum"] for dp in response.get("Datapoints", []))
    total_errors = sum(dp["Sum"] for dp in error_response.get("Datapoints", []))
    print("response:",response)
    print("error_response",error_response)
    print("total_invocations",total_invocations)
    print("total_errors",total_errors)
    if total_invocations == 0:
        return 100.0

    uptime = ((total_invocations - total_errors) / total_invocations) * 100
    return round(uptime, 2)


def get_rds_uptime(db_instance_identifier):
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(days=30)

    response = cloudwatch.get_metric_statistics(
        Namespace="AWS/RDS",
        MetricName="CPUUtilization",
        Dimensions=[
            {
                "Name": "DBInstanceIdentifier",
                "Value": db_instance_identifier
            }
        ],
        StartTime=start_time,
        EndTime=end_time,
        Period=86400,
        Statistics=["Average"]
    )

    datapoints = response.get("Datapoints", [])
    if not datapoints:
        return 0.0

    # If DB had connections → considered UP
    uptime = (len(datapoints) / 30) * 100
    return round(min(uptime, 100), 2)

# #indra
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import logging
import math

logger = logging.getLogger(__name__)

IST = ZoneInfo("Asia/Kolkata")
UTC = ZoneInfo("UTC")

def get_lambda_uptime_for_day(function_name, alias, date):

    start_ist = datetime.combine(
        date,
        datetime.min.time(),
        tzinfo=IST,
    )

    end_ist = start_ist + timedelta(days=1)

    start_time = start_ist.astimezone(UTC)
    end_time = end_ist.astimezone(UTC)

    dimensions = [
        {
            "Name": "FunctionName",
            "Value": function_name,
        },
        {
            "Name": "Resource",
            "Value": f"{function_name}:{alias}",
        },
    ]

    try:

        invocations = cloudwatch.get_metric_statistics(
            Namespace="AWS/Lambda",
            MetricName="Invocations",
            Dimensions=dimensions,
            StartTime=start_time,
            EndTime=end_time,
            Period=3600,
            Statistics=["Sum"],
        )

        errors = cloudwatch.get_metric_statistics(
            Namespace="AWS/Lambda",
            MetricName="Errors",
            Dimensions=dimensions,
            StartTime=start_time,
            EndTime=end_time,
            Period=3600,
            Statistics=["Sum"],
        )

        total_invocations = sum(
            dp.get("Sum", 0)
            for dp in invocations.get("Datapoints", [])
        )

        total_errors = sum(
            dp.get("Sum", 0)
            for dp in errors.get("Datapoints", [])
        )

        logger.info(
            f"{date} | Invocations={total_invocations} Errors={total_errors}"
        )

        if total_invocations == 0:
            return {
                "uptime_percentage": 100.0,
                "invocations": 0,
                "errors": 0,
            }

        successful = max(
            total_invocations - total_errors,
            0,
        )

        uptime = (
            successful / total_invocations
        ) * 100

        # uptime = math.floor(uptime * 100) / 100

        return {
            # "uptime_percentage": uptime,
            "uptime_percentage": round(uptime, 4),
            "invocations": int(total_invocations),
            "errors": int(total_errors),
        }

    except Exception as e:
        logger.exception(e)
        return None

# def get_lambda_uptime_for_day(function_name, date):
#     """
#     Returns Lambda uptime % for a single day
#     """
#     start_time = datetime.combine(date, datetime.min.time()).replace(tzinfo=timezone.utc)
#     end_time = start_time + timedelta(days=1)

#     invocations_resp = cloudwatch.get_metric_statistics(
#         Namespace="AWS/Lambda",
#         MetricName="Invocations",
#         Dimensions=[{"Name": "FunctionName", "Value": function_name}],
#         StartTime=start_time,
#         EndTime=end_time,
#         Period=86400,
#         Statistics=["Sum"],
#     )

#     errors_resp = cloudwatch.get_metric_statistics(
#         Namespace="AWS/Lambda",
#         MetricName="Errors",
#         Dimensions=[{"Name": "FunctionName", "Value": function_name}],
#         StartTime=start_time,
#         EndTime=end_time,
#         Period=86400,
#         Statistics=["Sum"],
#     )

#     total_invocations = (
#         invocations_resp["Datapoints"][0]["Sum"]
#         if invocations_resp["Datapoints"]
#         else 0
#     )

#     total_errors = (
#         errors_resp["Datapoints"][0]["Sum"]
#         if errors_resp["Datapoints"]
#         else 0
#     )

#     # SLA rule: no traffic = 100% uptime
#     if total_invocations == 0:
#         return 100.0

#     uptime = ((total_invocations - total_errors) / total_invocations) * 100
#     return round(uptime, 2)


def calculate_penalty(uptime):
    if uptime >= 95:
        return "No Penalty"
    elif uptime >= 90:
        return "5% Penalty"
    elif uptime >= 80:
        return "10% Penalty"
    else:
        return "15% Penalty"