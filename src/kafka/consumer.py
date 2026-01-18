from kafka import KafkaConsumer
import json
from src.input_loader import load_data
from src.streaming_engine import StreamBuffer
from src.main_drift_runner import run_stream_drift

train_df= load_data("data/train.csv")

buffer = StreamBuffer(batch_size=30)

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
    record= message.value
    print("Received:", record)

    ready= buffer.add(record)

    if ready:
        batch_df = buffer.get_dataframe()
        run_stream_drift(train_df,batch_df)

