import time
import os
import sys
from confluent_kafka import Consumer, KafkaError
from escpos.printer import Network

# Configuration for the Kafka consumer
conf = {
    "bootstrap.servers": "38.242.156.125:9092",
    "group.id": "TEST_GROUP",
    "auto.offset.reset": "earliest",
    "enable.auto.commit": False,  # Disable auto-commit
}

printer_ip = "192.168.178.177"


# Function to create a printer connection with retry logic
def create_printer_connection(retries=1, delay=1):
    for attempt in range(retries):
        try:
            return Network(printer_ip)
        except Exception as e:
            print(f"Attempt {attempt + 1}: Failed to connect to printer: {e}")
            time.sleep(delay)
    return None


epson = create_printer_connection()
consumer = Consumer(conf)
consumer.subscribe(["Mina"])


# Function to print a message
def print_message(message):
    global epson
    try:
        if epson is None:
            epson = create_printer_connection()
        if epson:
            print(message)
            # TODO
            # epson.text(message)
            # epson.cut()
            return True  # Return true if printed successfully
        else:
            return False  # Return false if printer connection failed
    except Exception as e:
        print(f"Printing error: {e}")
        epson = None  # Reset the printer connection
        return False  # Return false if an error occurred


try:
    print("Confluent v7 is running")
    while True:
        msg = consumer.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                continue
            else:
                print(f"Consumer error: {msg.error()}")
                break

        message = msg.value().decode("utf-8")
        callback = msg.callback()
        print("callback", callback)
        print(f"Received message: {message} from topic {msg.topic()}")

        # Retry printing the message until it is successful
        while True:
            if print_message(message):
                print(f"Message printed successfully: {message}")
                # Commit the message offset only after successful printing
                consumer.commit(asynchronous=False)
                break
            else:
                print(f"Failed to print message: {message}. Retrying in 1 seconds...")
                time.sleep(1)  # Wait for a while before retrying

except KeyboardInterrupt:
    print("Script interrupted by user. Exiting...")
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    consumer.close()
    print("Consumer closed.")
    # Reload the script
    print("Reloading script...")
    os.execv(sys.executable, ["python"] + sys.argv)
