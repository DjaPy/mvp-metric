from typing import Optional
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
    walking_steps: Optional[int]
    aerobic_steps: Optional[int]
    run_steps: Optional[int]
    burned_calories: Optional[float]
    distance: Optional[int]
    metric_datetime: datetime
    timestamp: Optional[datetime]
    user_id: int


class HeartRate(BaseModel):
    pulse: Optional[int]
    metric_datetime: Optional[int]
    timestamp: Optional[datetime]
    user_id: int


class TemperatureMeasurement(BaseModel):
    unit_temperature = Optional[UnitTemperature]
    temperature_measurement: Optional[float]
    metric_datetime: Optional[int]
    timestamp: Optional[datetime]
    user_id: int


class HeartRateVariability(BaseModel):
    pass
