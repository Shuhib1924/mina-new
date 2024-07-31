from confluent_kafka import Consumer, KafkaError
import json
import time

conf = {
    "bootstrap.servers": "38.242.156.125:9092",
    "group.id": "python-consumer",
    "auto.offset.reset": "earliest",
}

consumer = Consumer(conf)
consumer.subscribe(["Mina"])


def print_to_thermal_printer(message):
    # Implement the logic to print to the Epson thermal printer T20-III here
    # This is a placeholder function
    print(f"Printing to thermal printer: {message}")
    return True  # Return True if printing is successful, False otherwise


while True:
    msg = consumer.poll(1.0)

    if msg is None:
        continue
    if msg.error():
        if msg.error().code() == KafkaError._PARTITION_EOF:
            print("Reached end of partition")
        else:
            print(f"Error: {msg.error()}")
    else:
        try:
            message = json.loads(msg.value().decode("utf-8"))
            print(f"Received message: {message}")

            if print_to_thermal_printer(message):
                print("Message printed successfully")
                consumer.commit(msg)
            else:
                print("Failed to print message")
                # Message will be reprocessed in the next poll
        except Exception as e:
            print(f"Error processing message: {e}")
            # Message will be reprocessed in the next poll

    time.sleep(1)  # Add a small delay to avoid excessive CPU usage
