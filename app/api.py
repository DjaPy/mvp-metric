from typing import List
from datetime import datetime


from fastapi import APIRouter, HTTPException, status

from app.database.db import database
from app.schemas import (
    User,
    CreateResponseAllMetrics,
    CreateAllMetrics,
    AllMetricLast,
    AllMetricLastResponse,
)

from app.models import user, user_device, heart_rate, metric, temp_meas, device

router = APIRouter()


@router.get('/users/', response_model=List[User], status_code=status.HTTP_200_OK)
async def read_users():
    query = user.select()
    return await database.fetch_all(query)


@router.post(
    '/create_metric/',
    response_model=CreateResponseAllMetrics,
    status_code=status.HTTP_201_CREATED,
)
async def write_metrics(payload: CreateAllMetrics):
    metrics = payload.metrics
    heart_rate_m = payload.heart_rate
    temperature_measurement = payload.temperature_measurement
    query_device = device.select().where(
        device.mac_address == CreateAllMetrics.mac_address,
    )
    device_obj = database.fetch_one(query_device)

    query_user = user_device.select().where(
        user_device.device_id == device_obj.id,
    )
    user_obj = database.fetch_one(query_user)
    timestamp = datetime.now()

    if metrics:
        save_metric = []
        for metric_model in metrics:
            metric_dict = metric_model.dict()
            metric_dict['user_id'] = user_obj.id
            metric_dict['timestamp'] = timestamp
            save_metric.append(metric_dict)
        query_metrics = metric.insert().values(save_metric)
        await database.execute_many(query_metrics)
    if heart_rate_m:
        save_heart_rate = []
        for heart_rate_model in heart_rate_m:
            heart_rate_dict = heart_rate_model.dict()
            heart_rate_dict['user_id'] = user_obj.id
            heart_rate_dict['timestamp'] = timestamp
            save_heart_rate.append(heart_rate_dict)
        query_heart_rate = heart_rate.insert().values(save_heart_rate)
        await database.execute_many(query_heart_rate)
    if temperature_measurement:
        save_temp_meas = []
        for temp_meas_model in metrics:
            temp_meas_dict = temp_meas_model.dict()
            temp_meas_dict['user_id'] = user_obj.id
            temp_meas_dict['timestamp'] = timestamp
            save_temp_meas.append(temp_meas_dict)
        query_temp_meas = temp_meas.insert().values(save_temp_meas)
        await database.execute_many(query_temp_meas)

    response = CreateResponseAllMetrics()

    return response.dict()


@router.get(
    '/all_metric_now/{user_id}',
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