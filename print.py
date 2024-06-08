from escpos.printer import Network

# Set the IP address of the printer
printer_ip = '192.168.178.177'

# Initialize the network connection to the printer
epson = Network(printer_ip)

# Send data to the printer
epson.text("Test print from Python using Epson package via IP\n")
epson.cut()