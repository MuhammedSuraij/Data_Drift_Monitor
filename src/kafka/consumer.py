from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    "drift_stream",
    bootstrap_servers="localhost:9092",
    auto_offset_reset="earliest",
    enable_auto_commit=True,
    group_id="drift-monitor-group",
    value_deserializer=lambda x: json.loads(x.decode("utf-8"))
)

print("Kafka Consumer started...")

for message in consumer:
    print("Received:", message.value)
