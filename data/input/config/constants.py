import random

from log_sdk.common.action import Action
from log_sdk.common.status import Status

from config.utils import get_env

SENSOR_TYPES = ["Vibration", "Temperature", "Pressure", "Humidity", "Electrical"]

VALUE_DISTRIBUTIONS = {
    "Vibration": lambda: max(0, random.gauss(5.0, 1.0)),
    "Temperature": lambda: max(0, random.gauss(50, 10)),
    "Pressure": lambda: max(0, random.gauss(3, 0.5)),
    "Humidity": lambda: min(100, max(0, random.gauss(60, 15))),
    "Electrical": lambda: max(0, random.gauss(10.0, 2.0))
}

STATUSES = [Status.NORMAL, Status.WARNING, Status.CRITICAL, Status.FAULT]
ACTIONS = [Action.START, Action.STOP, Action.MAINTENANCE, Action.CALIBRATION]

ANOMALY_PROBABILITY = 0.01
ANOMALY_DISTRIBUTIONS = {
    "Vibration": lambda: max(0, random.gauss(50, 10)),
    "Temperature": lambda: max(0, random.gauss(150, 20)),
    "Pressure": lambda: max(0, random.gauss(10, 3)),
    "Humidity": lambda: min(100, max(0, random.gauss(10, 5))),
    "Electrical": lambda: max(0, random.gauss(50, 15))
}

NORMAL_DURATION_DISTRIBUTION = lambda: round(max(0.1, random.gauss(2.5, 1.0)), 2)
ANOMALY_DURATION_DISTRIBUTION = lambda: round(max(5.0, random.gauss(10.0, 3.0)), 2)

SENSOR_ID = get_env("SENSOR_ID")
KAFKA_BOOTSTRAP_SERVERS = get_env("KAFKA_BOOTSTRAP_SERVERS")
KAFKA_TOPIC = get_env("KAFKA_TOPIC", "")