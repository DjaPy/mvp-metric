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


class MetricResponse(BaseModel):
    total_steps: Optional[int]
    burned_calories: Optional[float]
    distance: Optional[int]


class CreateMetric(BaseModel):
    metric: List[Metric]
    mac_address: str


class HeartRate(BaseModel):
    pulse: Optional[List[int]]
    metric_datetime: Optional[datetime]


class CreateHeartRate(BaseModel):
    heart_rate: List[HeartRate]
    mac_address: str


class TemperatureMeasurement(BaseModel):
    unit_temperature: Optional[UnitTemperature]
    temperature_measurement: Optional[float]
    metric_datetime: Optional[datetime]


class CreateTemperatureMeasurement(BaseModel):
    temperature_measurement: List[TemperatureMeasurement]
    mac_address: str


class Sleep(BaseModel):
    sleep_minutes: Optional[int]
    metric_datetime: Optional[datetime]


class CreateSleep(BaseModel):
    sleep_list: List[Sleep]
    mac_address: str


class HeartRateVariability(BaseModel):
    pass


class CreateAllMetrics(BaseModel):
    user_id: Optional[int]
    mac_address: Optional[str]
    metrics: List[Metric]
    heart_rate: Optional[List[HeartRate]]
    temperature_measurement: Optional[List[TemperatureMeasurement]]


class CreateResponseMetrics(BaseModel):
    result: str = 'OK'


class AllMetricLast(BaseModel):
    metric: MetricResponse
    heart_rate: Optional[int]
    temperature_measurement: Optional[float]
    user: Optional[int]


class AllMetricLastResponse(BaseModel):
    all_metric_last: List[AllMetricLast]

