import time
import random

from log_sdk.logger_config import LoggerConfig
from log_sdk.common.channel import Channel
from log_sdk.common.data_center import DataCenter
from log_sdk.common.product import Product
from log_sdk.common.status import Status

from config.constants import (
    ACTIONS,
    ANOMALY_DISTRIBUTIONS,
    ANOMALY_PROBABILITY,
    SENSOR_TYPES,
    STATUSES,
    VALUE_DISTRIBUTIONS,
    NORMAL_DURATION_DISTRIBUTION,
    ANOMALY_DURATION_DISTRIBUTION
)
from config.utils import get_env
from config.logger import logger

class SensorProducer:
    def __init__(self):
        self.logger = LoggerConfig(
            sensor_id=get_env("SENSOR_ID"),
            KAFKA_BROKERS=get_env("KAFKA_BROKERS"),
            KAFKA_TOPIC=get_env("KAFKA_TOPIC"),
            kafka_enabled=True
        )

    def produce_sensor_data(self):
        """Runs the sensor data producer in a loop."""
        logger.info("Sensor data producer started...")
        while True:
            sensor_type = random.choice(SENSOR_TYPES)
            if random.random() < ANOMALY_PROBABILITY:
                duration = ANOMALY_DURATION_DISTRIBUTION()
                measurement = round(ANOMALY_DISTRIBUTIONS[sensor_type](), 2)
                status = Status.CRITICAL
            else:
                duration = NORMAL_DURATION_DISTRIBUTION()
                measurement = round(VALUE_DISTRIBUTIONS[sensor_type](), 2)
                status = random.choices(STATUSES, weights=[0.9, 0.05, 0.05, 0.0])[0]
            
            action = random.choices(ACTIONS, weights=[0.95, 0.05, 0.0, 0.0])[0]

            self.logger.update_machine_status(action)
            
            log_function = {
                "Vibration": self.logger.log_vibration,
                "Temperature": self.logger.log_temperature,
                "Pressure": self.logger.log_pressure,
                "Humidity": self.logger.log_humidity,
                "Electrical": self.logger.log_electrical
            }.get(sensor_type)

            if log_function:
                log_function(
                    channel=Channel.SENSOR,
                    data_center=DataCenter.FACTORY_1,
                    duration=duration,
                    measurement=measurement,
                    product=Product.MACHINE_MONITORING,
                    status=status,
                )

            time.sleep(max(0.1, random.gauss(1.0, 0.5)))
