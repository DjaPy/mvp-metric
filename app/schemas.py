from typing import Optional, List
from datetime import date, datetime
from enum import Enum

from pydantic import BaseModel


class UnitTemperature(str, Enum):
    celsius = 'Celsius'
    fahrenheit = 'Fahrenheit'


class User(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    device_mac: str
    birthday: date


class Metric(BaseModel):
    # walking_steps: Optional[int]
    # aerobic_steps: Optional[int]
    # run_steps: Optional[int]
    total_steps: Optional[int]
    burned_calories: Optional[float]
    distance: Optional[int]
    metric_datetime: datetime


class HeartRate(BaseModel):
    pulse: Optional[int]
    metric_datetime: Optional[datetime]


class TemperatureMeasurement(BaseModel):
    unit_temperature: Optional[UnitTemperature]
    temperature_measurement: Optional[float]
    metric_datetime: Optional[datetime]


class HeartRateVariability(BaseModel):
    pass


class CreateAllMetrics(BaseModel):
    user_id: Optional[int]
    mac_address: Optional[str]
    metrics: List[Metric]
    heart_rate: Optional[List[HeartRate]]
    temperature_measurement: Optional[List[TemperatureMeasurement]]


class CreateResponseAllMetrics(BaseModel):
    result: str = 'OK'
