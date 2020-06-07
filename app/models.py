from sqlalchemy import (
    Column,
    Table,
    MetaData,
    Integer,
    String,
    Boolean,
    Float,
    DateTime,
    ForeignKey,
)

metadata = MetaData()

user = Table(
    "user", metadata,

    Column("id", Integer, primary_key=True),
    Column("first_name", String),
    Column("last_name", String),
    Column("device_mac", String),
    Column("birthday", String, )
)

device = Table(
    "device", metadata,

    Column("id", Integer, primary_key=True),
    Column("changed", DateTime),
    Column("mac_address", String),

)

user_device = Table(
    'user_device', metadata,

    Column('id', Integer, primary_key=True),
    Column('changed', DateTime),
    Column('user_id', Integer, ForeignKey('user.id', ondelete='CASCADE')),
    Column('device_id', Integer, ForeignKey('device.id', ondelete='CASCADE'))
)


metric = Table(
    "metric", metadata,

    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("timestamp", DateTime),
    Column("metric_datetime", DateTime),
    Column("walking_steps", Integer),
    Column("run_steps", Integer),
    Column('total_steps', Integer),
    Column("aerobic_steps", Integer),
    Column("distance", Integer),
    Column("burned_calories", Integer),
    Column("user_id", Integer, ForeignKey("user.id")),
)

heart_rate = Table(
    "heart_rate", metadata,

    Column("id", Integer, primary_key=True),
    Column("timestamp", DateTime),
    Column("metric_datetime", DateTime),
    Column("pulse", Integer),
    Column("user_id", Integer, ForeignKey("user.id")),
)

temp_meas = Table(
    "temperature_measurement", metadata,

    Column("id", Integer, primary_key=True),
    Column("timestamp", DateTime),
    Column("metric_datetime", DateTime),
    Column("temperature_measurement", Float),
    Column('unit_temperature', String),
    Column("user_id", Integer, ForeignKey("user.id"))
)

sleep = Table(
    "sleep", metadata,

    Column("id", Integer, primary_key=True),
    Column("timestamp", DateTime),
    Column("metric_datetime", DateTime),
    Column("sleep_minutes", Integer),
    Column("user_id", Integer, ForeignKey("user.id"))
)
