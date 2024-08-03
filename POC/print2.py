from escpos.printer import Network

# Initialize the printer using its IP address
printer = Network("192.168.178.177")  # Replace with your printer's IP address


def set_text_style(style):
    if style == "bold":
        printer._raw(b"\x1B\x45\x01")  # Enable bold
    else:
        printer._raw(b"\x1B\x45\x00")  # Disable bold

    if style == "italic":
        printer._raw(b"\x1B\x34")  # Enable italic
    else:
        printer._raw(b"\x1B\x35")  # Disable italic


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
    printer._raw(bytes([0x1D, 0x21, command_byte]))


def set_text_alignment(alignment):
    if alignment == "center":
        printer._raw(b"\x1B\x61\x01")  # Center alignment
    elif alignment == "end":
        printer._raw(b"\x1B\x61\x02")  # Right alignment
    elif alignment == "indent2":
        printer._raw(b"\x1B\x61\x00")  # Left alignment
        printer._raw(b"\x1B\x6C" + bytes([2]))  # Set left margin to ~2 characters
    elif alignment == "indent4":
        printer._raw(b"\x1B\x61\x00")  # Left alignment
        printer._raw(b"\x1B\x6C" + bytes([4]))  # Set left margin to ~4 characters
    elif alignment == "indent6":
        printer._raw(b"\x1B\x61\x00")  # Left alignment
        printer._raw(b"\x1B\x6C" + bytes([6]))  # Set left margin to ~6 characters
    elif alignment == "start":
        printer._raw(b"\x1B\x61\x00")  # Left alignment (default)
        printer._raw(b"\x1B\x6C" + bytes([0]))  # Reset left margin
    else:
        printer._raw(b"\x1B\x61\x00")  # Left alignment (default)
        printer._raw(b"\x1B\x6C" + bytes([0]))  # Reset left margin


def text4(text, size="normal", style="normal", alignment="start"):
    set_text_style(style)
    set_text_size(size)  # Set text size
    set_text_alignment(alignment)  # Set text alignment

    # Print the text
    printer.text(text + "\n")

    # Reset to default settings
    printer._raw(b"\x1B\x21\x00")  # Reset size and style settings
    printer._raw(b"\x1B\x61\x00")  # Reset alignment to left


text4("Text", "5:5", "bold", "start")
text4("Text", "5:5", "bold", "indent2")
text4("Text", "5:5", "bold", "indent4")
text4("Text", "5:5", "bold", "indent6")
text4("Text", "5:5", "bold", "start")

# Cut the paper
printer.cut()

# Close the connection
printer.close()
