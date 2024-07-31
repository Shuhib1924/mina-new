from escpos.printer import Network

# Initialize the network connection to the printer
epson = Network("192.168.178.177")

# Send data to the printer
epson.text("Test print from Python using Epson package via IP\n")
epson.cut()
