from app.models import device, user_device
from datetime import timedelta, datetime


async def get_user_by_device(database, mac_address):
    query_device = device.select().where(
        device.c.mac_address == mac_address,
    )
    device_obj = await database.fetch_one(query_device)

    query_user = user_device.select().where(
        user_device.c.device_id == device_obj['id'],
    )
    return await database.fetch_one(query_user)


def get_average_pulse_in_minute(heart_rate_models, user_id, now):
    """Gets a list of heart rate records in 2 minutes

    :param ten_second_pulse_list:
    :return:
    """
    first_metric_datetime = heart_rate_models.metric_datetime
    second_metric_datetime = first_metric_datetime + timedelta(minutes=1)
    count_of_minutes_in_list = 2

    middle_pulse_list = round(len(heart_rate_models.pulse) / count_of_minutes_in_list)

    fisrt_list_pulse = heart_rate_models.pulse[:middle_pulse_list]
    second_list_pulse = heart_rate_models.pulse[middle_pulse_list:]

    pulse_of_first_minute = round(sum(fisrt_list_pulse) / len(fisrt_list_pulse))
    pulse_of_second_minute = round(sum(second_list_pulse) / len(second_list_pulse))

    return [
        {
            "timestamp": now,
            "metric_datetime": first_metric_datetime,
            "pulse": pulse_of_first_minute,
            "user_id": user_id,
        },
        {
            "timestamp": now,
            "metric_datetime": second_metric_datetime,
            "pulse": pulse_of_second_minute,
            "user_id": user_id,
        },
    ]
