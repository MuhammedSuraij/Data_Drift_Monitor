from kafka import KafkaProducer
import json
import time
import random

producer = KafkaProducer(
    bootstrap_servers="localhost:9092",   # ✅ FIXED
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

print("Kafka Producer started...")

rnum=0
while rnum!=60:
    rnum=rnum+1
    record = {
        "age": random.randint(18, 60),
        "amount": random.randint(100, 1000),
        "category": random.choice(["a", "b", "fraud"])
    }

    producer.send("drift_stream", value=record)
    print("Sent:", record)

    time.sleep(2)
