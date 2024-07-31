from confluent_kafka import Producer
import json

# Configuration for the Kafka producer
conf = {
    "bootstrap.servers": "38.242.156.125:9092",
    "compression.type": "gzip",
    "retries": 3,
    "retry.backoff.ms": 1000,
    "batch.num.messages": 32768,
    "linger.ms": 5,
    "queue.buffering.max.messages": 100000,
    "queue.buffering.max.kbytes": 33554432,  # 32 MB
}

# Create the Kafka producer
producer = Producer(conf)


# JSON serializer function
def json_serializer(data):
    return json.dumps(data).encode("utf-8")


# Delivery report callback function
def delivery_report(err, msg):
    if err is not None:
        print(f"Message delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}]")


# Example messages to send
messages = [
    {"key": "value1"},
    {"key": "value2"},
    # {"key": "value3"},
]

# Produce messages asynchronously
for message in messages:
    producer.produce("Mina", value=json_serializer(message), callback=delivery_report)
    producer.poll(0)  # Trigger delivery reports

# Wait for any outstanding messages to be delivered
producer.flush()
