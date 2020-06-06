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
    AllMetricLast,
    AllMetricLastResponse,
)
from app.utils import get_user_by_device, get_average_pulse_in_minute
from app.models import user, user_device, heart_rate, metric, temp_meas, device

templates = Jinja2Templates(directory="templates")

router = APIRouter()


@router.get("/")
async def main(request: Request):
    return templates.TemplateResponse("main.html", {"request": request, "id": id})


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
        heart_rate_duo = get_average_pulse_in_minute(heart_rate_model, user_obj['user_id'], timestamp)
        save_heart_rate.append(heart_rate_duo[0])
        save_heart_rate.append(heart_rate_duo[1])
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


@router.get(
    '/all_metric_now/',
    response_model=AllMetricLastResponse,
    status_code=status.HTTP_200_OK,
)
async def get_last_metrics():
    query_users = user.select()
    users = await database.fetch_all(query_users)
    users_ids = []
    for user_obj in users:
        users_ids.append(user_obj.id)

    query_metric_by_user = user.select().where(user.c.id_in(users_ids))