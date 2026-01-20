from fastapi import FastAPI
from kafka import KafkaProducer
import json

app= FastAPI(title="Drift Data Ingestion API")

producer= KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer= lambda x: json.dumps(x).encode("utf-8")
)

TOPIC = "drift_stream"

@app.post("/ingest")
def ingest_record(record: dict):

    producer.send(TOPIC, record)
    producer.flush()

    return {
        "status": "send_to_kafka",
        "record": record
    }

