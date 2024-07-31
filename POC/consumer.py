from kafka import KafkaConsumer
from escpos.printer import Network


PRINTER_IP = "192.168.178.177"
printer = Network(PRINTER_IP)

consumer = KafkaConsumer(
    "TOPIC",
    bootstrap_servers=["38.242.156.125:9092"],
    auto_offset_reset="latest",
)

print("consumer has started...")
for message in consumer:
    print(message.value.decode("utf-8"))
    printer.text(message.value.decode("utf-8"))
    printer.cut()
