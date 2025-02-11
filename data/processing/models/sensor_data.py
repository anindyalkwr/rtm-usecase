import dataclasses

from pyflink.common import Types, Row

@dataclasses.dataclass
class SensorData:
    timestamp: str
    sensor_id: str
    channel: str
    data_center: str
    duration: float
    measurement: float
    product: str
    status: str
    type: str     # Note: 'type' is a built-in name, but it is allowed as a field name.
    unit: str
    metadata: str

    def asdict(self):
        return dataclasses.asdict(self)

    @classmethod
    def from_row(cls, row: Row):
        return cls(
            timestamp=row.timestamp,
            sensor_id=row.sensor_id,
            channel=row.channel,
            data_center=row.data_center,
            duration=row.duration,
            measurement=row.measurement,
            product=row.product,
            status=row.status,
            type=row.type,
            unit=row.unit,
            metadata=row.metadata,
        )

    def to_row(self):
        return Row(
            timestamp=self.timestamp,
            sensor_id=self.sensor_id,
            channel=self.channel,
            data_center=self.data_center,
            duration=self.duration,
            measurement=self.measurement,
            product=self.product,
            status=self.status,
            type=self.type,
            unit=self.unit,
            metadata=self.metadata,
        )

    @staticmethod
    def get_value_type_info():
        return Types.ROW_NAMED(
            field_names=[
                "timestamp",
                "sensor_id",
                "channel",
                "data_center",
                "duration",
                "measurement",
                "product",
                "status",
                "type",
                "unit",
                "metadata",
            ],
            field_types=[
                Types.STRING(),
                Types.STRING(),
                Types.STRING(),
                Types.STRING(),
                Types.FLOAT(),
                Types.FLOAT(),
                Types.STRING(),
                Types.STRING(),
                Types.STRING(),
                Types.STRING(),
                Types.STRING(),
            ],
        )
