from typing import List


from fastapi import APIRouter, HTTPException, status

from app.database.db import database
from app.schemas import (
    User,
    CreateResponseAllMetrics,
    CreateAllMetrics,
)

from app.models import user, user_device, heart_rate, metric, temp_meas

router = APIRouter()


@router.get("/users/", response_model=List[User], status_code=status.HTTP_200_OK)
async def read_users():
    query = user.select()
    return await database.fetch_all(query)


@router.post(
    "/create_metric/",
    response_model=CreateResponseAllMetrics,
    status_code=status.HTTP_201_CREATED,
)
async def write_metrics(payload: CreateAllMetrics):
    metrics = payload.metrics
    heart_rate = payload.heart_rate
    temperature_measurement = payload.temperature_measurement

    # if metrics:
    #     query_metrics =
    # if heart_rate:
    #     query_heart_rate =
    # if temperature_measurement:
    #     query_temperature_measurement
    response = CreateResponseAllMetrics()

    return response.dict()
