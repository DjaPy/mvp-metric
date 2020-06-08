from typing import List
from datetime import datetime


from fastapi import APIRouter, Request, HTTPException, status
from fastapi.templating import Jinja2Templates

from app.database.db import database
from app.schemas import (
    User,
    CreateResponseMetrics,
    CreateHeartRate,
    CreateMetric,
    CreateTemperatureMeasurement,
    CreateSleep,
    AllMetricLast,
    AllMetricLastResponse,
    MetricResponse,
)
from app.utils import (
    get_user_by_device,
    get_average_pulse_in_minute,
    get_metric_of_day,
    get_sleep,
)
from app.models import user, sleep, heart_rate, metric, temp_meas

templates = Jinja2Templates(directory="templates")

router = APIRouter()


@router.get("/")
async def main(request: Request):
    return templates.TemplateResponse("main.html", {"request": request, "id": id})


@router.get("/metric")
async def metric(request: Request):
    query_users = user.select()
    users = await database.fetch_all(query_users)
    all_metric_list = []
    for user_obj in users:
        metric_of_day = await get_metric_of_day(database, user_obj['id'])
        metric_response = MetricResponse(
            total_steps=metric_of_day['steps'],
            burned_calories=metric_of_day['burned_calories'],
            distance=metric_of_day['distance'],
        )
        query_heart_rate_current = heart_rate.select().where(
            heart_rate.c.user_id == user_obj['id'],
        )
        heart_rate_current = await database.fetch_one(query_heart_rate_current)
        query_temperature_measurement = temp_meas.select().where(temp_meas.c.user_id == user_obj['id'])
        temp_meas_current = await database.fetch_one(query_temperature_measurement)
        sleep_of_day = await get_sleep(database, user_obj['id'])
        all_metric = AllMetricLast(
            metric=metric_response,
            heart_rate=heart_rate_current['pulse'],
            temperature_measurement=temp_meas_current['temperature_measurement'],
            sleep=sleep_of_day,
            user=user_obj['id'],
        )
        all_metric_list.append(all_metric)

    all_metrics = AllMetricLastResponse(
        all_metric_last=all_metric_list
    )
    response_dict = {
        'request': request
    }
    response_dict.update(all_metrics.dict())
    return templates.TemplateResponse('metric.html', response_dict)


@router.get('/users/', response_model=List[User], status_code=status.HTTP_200_OK)
async def read_users():
    query = user.select()
    return await database.fetch_all(query)


@router.post(
    '/create_metric/',
    response_model=CreateResponseMetrics,
    status_code=status.HTTP_201_CREATED,
)
async def write_metrics(payload: CreateMetric):
    if not payload.mac_address or not payload.metric:
        raise HTTPException
    metrics = payload.metric
    mac_address = payload.mac_address
    user_obj = await get_user_by_device(database, mac_address)
    timestamp = datetime.now()

    save_metric = []
    for metric_model in metrics:
        metric_dict = metric_model.dict()
        metric_dict['user_id'] = user_obj['user_id']
        metric_dict['timestamp'] = timestamp
        save_metric.append(metric_dict)
    query_metrics = metric.insert().values(save_metric)
    await database.execute(query_metrics)

    response = CreateResponseMetrics()

    return response.dict()


@router.post(
    '/create_heart_rate/',
    response_model=CreateResponseMetrics,
    status_code=status.HTTP_201_CREATED,
)
async def write_heart_rate(payload: CreateHeartRate):
    if not payload.heart_rate or not payload.mac_address:
        raise HTTPException
    heart_rate_m = payload.heart_rate
    mac_address = payload.mac_address
    user_obj = await get_user_by_device(database, mac_address)
    timestamp = datetime.now()
    save_heart_rate = []
    for heart_rate_model in heart_rate_m:
        # heart_rate_duo = get_average_pulse_in_minute(heart_rate_model, user_obj['user_id'], timestamp)
        # save_heart_rate.append(heart_rate_duo[0])
        # save_heart_rate.append(heart_rate_duo[1])
        heart_rate_dict = heart_rate_model.dict()
        heart_rate_dict['user_id'] = user_obj['user_id']
        heart_rate_dict['timestamp'] = timestamp
        save_heart_rate.append(heart_rate_dict)

    query_heart_rate = heart_rate.insert().values(save_heart_rate)
    await database.execute(query_heart_rate)

    response = CreateResponseMetrics()

    return response.dict()


@router.post(
    '/create_temperature/',
    response_model=CreateResponseMetrics,
    status_code=status.HTTP_201_CREATED,
)
async def write_temperature_measurement(payload: CreateTemperatureMeasurement):
    if not payload.temperature_measurement or not payload.mac_address:
        raise HTTPException
    temperature_m = payload.temperature_measurement
    mac_address = payload.mac_address
    user_obj = await get_user_by_device(database, mac_address)
    timestamp = datetime.now()

    save_temperature = []
    for temperature_model in temperature_m:
        temperature_dict = temperature_model.dict()
        temperature_dict['user_id'] = user_obj['user_id']
        temperature_dict['timestamp'] = timestamp
        save_temperature.append(temperature_dict)
    query_temp_meas = temp_meas.insert().values(save_temperature)
    await database.execute(query_temp_meas)

    response = CreateResponseMetrics()

    return response.dict()


@router.post(
    '/create_sleep/',
    response_model=CreateResponseMetrics,
    status_code=status.HTTP_201_CREATED,
)
async def write_sleep(payload: CreateSleep):
    if not payload.sleep_list or not payload.mac_address:
        raise HTTPException
    sleep_m = payload.sleep_list
    mac_address = payload.mac_address
    user_obj = await get_user_by_device(database, mac_address)
    timestamp = datetime.now()

    save_sleep = []
    for sleep_model in sleep_m:
        sleep_dict = sleep_model.dict()
        sleep_dict['user_id'] = user_obj['user_id']
        sleep_dict['timestamp'] = timestamp
        save_sleep.append(sleep_dict)
    query_sleep = sleep.insert().values(save_sleep)
    await database.execute(query_sleep)

    response = CreateResponseMetrics()

    return response.dict()


@router.get(
    '/all_metric_now/',
    response_model=AllMetricLastResponse,
    status_code=status.HTTP_200_OK,
)
async def get_last_metrics():
    query_users = user.select()
    users = await database.fetch_all(query_users)
    all_metric_list = []
    for user_obj in users:
        metric_of_day = await get_metric_of_day(database, user_obj['id'])
        metric_response = MetricResponse(
            total_steps=metric_of_day['steps'],
            burned_calories=metric_of_day['burned_calories'],
            distance=metric_of_day['distance'],
        )
        query_heart_rate_current = heart_rate.select().where(
            heart_rate.c.user_id == user_obj['id'],
        )
        heart_rate_current = await database.fetch_one(query_heart_rate_current)
        query_temperature_measurement = temp_meas.select().where(temp_meas.c.user_id == user_obj['id'])
        temp_meas_current = await database.fetch_one(query_temperature_measurement)
        sleep_of_day = await get_sleep(database, user_obj['id'])
        all_metric = AllMetricLast(
            metric=metric_response,
            heart_rate=heart_rate_current['pulse'],
            temperature_measurement=temp_meas_current['temperature_measurement'],
            sleep=sleep_of_day,
            user=user_obj['id'],
        )
        all_metric_list.append(all_metric)

    all_metrics = AllMetricLastResponse(
        all_metric_last=all_metric_list
    ).dict()
    return all_metrics
