import threading
import uvicorn
from fastapi import FastAPI
from producer import SensorProducer

app = FastAPI()
producer = SensorProducer()

def start_producer():
    producer_thread = threading.Thread(target=producer.produce_sensor_data, daemon=True)
    producer_thread.start()

start_producer()

@app.get("/ping")
def health_check():
    return {"status": "ok", "message": "Sensor producer is running"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
