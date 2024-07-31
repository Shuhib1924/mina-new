import time
from kafka import KafkaProducer

producer = KafkaProducer(bootstrap_servers=["38.242.156.125:9092"])
producer.send("TOPIC", b"new2")
time.sleep(0.1)
