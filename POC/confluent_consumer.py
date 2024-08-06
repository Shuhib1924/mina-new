import time
import os
import sys
from confluent_kafka import Consumer, KafkaError
from escpos.printer import Network, Usb
import json

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


def set_text_style(style):
    if style == "bold":
        epson._raw(b"\x1B\x45\x01")  # Enable bold
    else:
        epson._raw(b"\x1B\x45\x00")  # Disable bold

    if style == "italic":
        epson._raw(b"\x1B\x34")  # Enable italic
    else:
        epson._raw(b"\x1B\x35")  # Disable italic


def set_text_size(scale):
    # Define size mappings for various text sizes
    # The maximum multiplier for both height and width is 8
    size_mapping = {
        "1:1": (1, 1),  # Normal size
        "2:2": (2, 2),  # Double height and width
        "2:3": (2, 3),  # 2x height, 3x width
        "2:4": (2, 4),  # 2x height, 4x width
        "3:3": (3, 3),  # 3x height, 3x width
        "3:4": (3, 4),  # 3x height, 4x width
        "3:5": (3, 5),  # 3x height, 5x width
        "3:6": (3, 6),  # 3x height, 6x width
        "3:7": (3, 7),  # 3x height, 7x width
        "4:4": (4, 4),  # 4x height, 4x width
        "4:5": (4, 5),  # 4x height, 5x width
        "4:6": (4, 6),  # 4x height, 6x width
        "4:7": (4, 7),  # 4x height, 7x width
        "5:5": (5, 5),  # 5x height, 5x width
        "5:6": (5, 6),  # 5x height, 6x width
        "5:7": (5, 7),  # 5x height, 7x width
        "6:6": (6, 6),  # 6x height, 6x width
        "6:7": (6, 7),  # 6x height, 7x width
        "7:7": (7, 7),  # 7x height, 7x width
        "8:8": (8, 8),  # Maximum size: 8x height, 8x width
    }

    # Get the height and width multipliers from the mapping
    # Default to (1, 1) if the scale is not found in the mapping
    height_multiplier, width_multiplier = size_mapping.get(scale, (1, 1))

    # Ensure multipliers are within the valid range (1-8)
    height_multiplier = max(1, min(8, height_multiplier))
    width_multiplier = max(1, min(8, width_multiplier))

    # Calculate the command byte
    # The height multiplier uses bits 4-7, the width multiplier uses bits 0-3
    command_byte = ((height_multiplier - 1) << 4) | (width_multiplier - 1)

    # Send the GS ! n command to set text size
    epson._raw(bytes([0x1D, 0x21, command_byte]))


def set_text_alignment(alignment):
    if alignment == "center":
        epson._raw(b"\x1B\x61\x01")  # Center alignment
    elif alignment == "end":
        epson._raw(b"\x1B\x61\x02")  # Right alignment
    elif alignment == "indent2":
        epson._raw(b"\x1B\x61\x00")  # Left alignment
        epson._raw(b"\x1B\x44\x02\x00")  # Set left margin to 2 characters
    elif alignment == "indent4":
        epson._raw(b"\x1B\x61\x00")  # Left alignment
        epson._raw(b"\x1B\x44\x04\x00")  # Set left margin to 4 characters
    elif alignment == "indent6":
        epson._raw(b"\x1B\x61\x00")  # Left alignment
        epson._raw(b"\x1B\x44\x06\x00")  # Set left margin to 6 characters
    elif alignment == "start":
        epson._raw(b"\x1B\x61\x00")  # Left alignment (default)
        epson._raw(b"\x1B\x44\x00")  # Reset left margin
    else:
        epson._raw(b"\x1B\x61\x00")  # Left alignment (default)
        epson._raw(b"\x1B\x44\x00")  # Reset left margin


def text4(text, size="normal", style="normal", alignment="start"):
    set_text_style(style)
    set_text_size(size)  # Set text size
    set_text_alignment(alignment)  # Set text alignment

    # Print the text
    epson.text(text + "\n")

    # Reset to default settings
    epson._raw(b"\x1B\x21\x00")  # Reset size and style settings
    epson._raw(b"\x1B\x61\x00")  # Reset alignment to left


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
            # ? checks!
            # try:
            #     # print(message)
            #     print(type(message))
            #     # $if there is an error deactivate json.loads
            #     dict_message = json.loads(message)
            #     print("type", type(dict_message))
            #     # print("dict_message", dict_message)
            #     # % check datatype of after converting to json
            #     print(f"{dict_message["order"]}")
            #     print(f"{dict_message["order"][0]['form_data']}")
            #     print(f"{dict_message["order"][0]['form_data']['pickupTime']}")
            #     print(f"{dict_message["order"][0]['form_data']['name']}")
            #     print(f"{dict_message["order"][0]['form_data']['phone']}")
            #     # print(f"{dict_message["order"][1]['products']}")
            #     for i in dict_message["order"][1]['products']:
            #         print(i["user"])
            #         print(i["product"])
            #         for j in i["query_set"]:
            #             print(j["query"])
            #             for k in j["variation_set"]:
            #                 print(k)
            #         print("\n")
            # except Exception as e:
            #     print(f"Error processing message: {e}")
            dict_message = json.loads(message)
            # print("if its error print this instead the printer \n",message)
            text4(f"\n\n\n\n", "7:7", "bold", "center")
            text4(f"{dict_message["order"][0]['form_data']['pickupTime']}", "7:7", "bold", "center")
            text4(f"{dict_message["order"][0]['form_data']['currentTime']}", "2:4", "bold", "end")
            text4(f"---------", "5:5", "bold", "center")
            text4(f"{dict_message["order"][0]['form_data']['daily_id']}", "5:5", "bold", "center")
            text4(f"---------", "5:5", "bold", "center")
            text4(f"{dict_message["order"][0]['form_data']['first_name']} {dict_message["order"][0]['form_data']['last_name']}", "4:4", "bold", "center")
            text4(f"{dict_message["order"][0]['form_data']['phone']}", "3:4", "bold", "center")
            for i in dict_message["order"][1]["products"]:
                text4(f'{i["user"].upper()}', "3:5", "bold", "start")
                text4(f'  {i["product"]}', "3:3", "normal", "indent2")
                for j in i["query_set"]:
                    text4(f'    {j["query"]}', "2:3", "normal", "indent4")
                    for k in j["variation_set"]:
                        text4(f"       -{k}", "2:2", "normal", "indent6")
            epson.cut()
            epson.close()
            return True  # Return true if printed successfully
        else:
            return False  # Return false if printer connection failed
    except Exception as e:
        print(f"Printing error: {e}")
        epson = None  # Reset the printer connection
        return False  # Return false if an error occurred


try:
    print("Confluent v17 is running")
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
        print(f"Received message: {message} from topic {msg.topic()}")

        # Retry printing the message until it is successful
        while True:
            if print_message(message):
                print(f"Message printed successfully!")
                # print(f"Message printed successfully: {message}")
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
