# from escpos.printer import Network

# # Initialize the printer using its IP address
# printer = Network("192.168.178.177")  # Replace with your printer's IP address


# def set_text_style(style):
#     if style == "bold":
#         printer._raw(b"\x1B\x45\x01")  # Enable bold
#     else:
#         printer._raw(b"\x1B\x45\x00")  # Disable bold

#     if style == "italic":
#         printer._raw(b"\x1B\x34")  # Enable italic
#     else:
#         printer._raw(b"\x1B\x35")  # Disable italic


# def set_text_size(scale):
#     size_mapping = {
#         "normal": b"\x1B\x21\x00",  # Normal size
#         "double": b"\x1D\x21\x10",  # Double height and width
#         "triple": b"\x1D\x21\x20",  # Triple height and width
#         "quadruple": b"\x1D\x21\x30",  # Quadruple height and width
#         "six_times": b"\x1D\x21\x40",  # Six times height and width
#         "eight_times": b"\x1D\x21\x50",  # Eight times height and width
#         "ten_times": b"\x1D\x21\x60",  # Ten times height and width
#     }
#     return size_mapping.get(scale, size_mapping["normal"])


# def set_text_alignment(alignment):
#     if alignment == "center":
#         printer._raw(b"\x1B\x61\x01")  # Center alignment
#     elif alignment == "end":
#         printer._raw(b"\x1B\x61\x02")  # Right alignment
#     else:
#         printer._raw(b"\x1B\x61\x00")  # Left alignment (default)


# def print_text_with_style_size_and_alignment(
#     text, size="normal", style="normal", alignment="start"
# ):
#     set_text_style(style)
#     printer._raw(set_text_size(size))  # Set text size
#     set_text_alignment(alignment)  # Set text alignment

#     # Print the text
#     printer.text(text + "\n")

#     # Reset to default settings
#     printer._raw(b"\x1B\x21\x00")  # Reset size and style settings
#     printer._raw(b"\x1B\x61\x00")  # Reset alignment to left


# # Example usage
# print_text_with_style_size_and_alignment("Normal Text", "normal", "normal", "start")
# print_text_with_style_size_and_alignment("Bold Text", "double", "bold", "center")
# print_text_with_style_size_and_alignment("Italic Text", "triple", "italic", "end")
# print_text_with_style_size_and_alignment(
#     "Quadruple Size Text", "quadruple", "normal", "center"
# )
# print_text_with_style_size_and_alignment(
#     "Six Times Size Text", "six_times", "bold", "start"
# )
# print_text_with_style_size_and_alignment(
#     "Eight Times Size Text", "eight_times", "italic", "end"
# )
# print_text_with_style_size_and_alignment(
#     "Ten Times Size Text", "ten_times", "bold", "center"
# )

# # Cut the paper
# printer.cut()

# # Close the connection
# printer.close()


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
    height_width_mapping = {
        "normal": (1, 1),  # Normal size
        "double": (2, 2),  # Double height and width
        "triple": (3, 3),  # Triple height and width
        "quadruple": (4, 4),  # Quadruple height and width
        "six_times": (6, 6),  # Six times height and width
        "eight_times": (8, 8),  # Eight times height and width
        "ten_times": (10, 10),  # Ten times height and width
    }

    height, width = height_width_mapping.get(scale, (1, 1))

    # Set the heights and widths
    printer._raw(bytes([0x1D, 0x21, (height << 4) | width]))  # GS ! n


def set_text_alignment(alignment):
    if alignment == "center":
        printer._raw(b"\x1B\x61\x01")  # Center alignment
    elif alignment == "end":
        printer._raw(b"\x1B\x61\x02")  # Right alignment
    else:
        printer._raw(b"\x1B\x61\x00")  # Left alignment (default)


def print_text_with_style_size_and_alignment(
    text, size="normal", style="normal", alignment="start"
):
    set_text_style(style)
    set_text_size(size)  # Set text size
    set_text_alignment(alignment)  # Set text alignment

    # Print the text
    printer.text(text + "\n")

    # Reset to default settings
    printer._raw(b"\x1B\x21\x00")  # Reset size and style settings
    printer._raw(b"\x1B\x61\x00")  # Reset alignment to left


# Example usage
print_text_with_style_size_and_alignment("Normal Text", "normal", "normal", "start")
print_text_with_style_size_and_alignment("Bold Text", "double", "bold", "center")
print_text_with_style_size_and_alignment("Italic Text", "triple", "italic", "end")
print_text_with_style_size_and_alignment(
    "Quadruple Size Text", "quadruple", "normal", "center"
)
print_text_with_style_size_and_alignment(
    "Six Times Size Text", "six_times", "bold", "start"
)
print_text_with_style_size_and_alignment(
    "Eight Times Size Text", "eight_times", "italic", "end"
)
print_text_with_style_size_and_alignment(
    "Ten Times Size Text", "ten_times", "bold", "center"
)

# Cut the paper
printer.cut()

# Close the connection
printer.close()
