import asyncio
import uvicorn

from fastapi import FastAPI
from contextlib import asynccontextmanager
from producer import SensorProducer

@asynccontextmanager
async def lifespan(app: FastAPI):
    producer = SensorProducer()
    await producer.initialize()

    app.state.producer = producer
    app.state.producer_task = asyncio.create_task(producer.produce_sensor_data())
    
    yield
    
    app.state.producer_task.cancel()
    await producer.logger.close()

app = FastAPI(lifespan=lifespan)

@app.get("/ping")
async def health_check():
    return {"status": "ok", "message": "Sensor producer is running"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
