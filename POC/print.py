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
epson = Network("192.168.178.177")  # Replace with your printer's IP address


def set_text_alignment(alignment, indent=0):
    # Reset alignment and margin first
    epson._raw(b"\x1B\x61\x00")  # Left alignment (default)
    epson._raw(b"\x1B\x6C\x00")  # Reset left margin

    if alignment == "center":
        epson._raw(b"\x1B\x61\x01")  # Center alignment
    elif alignment == "end":
        epson._raw(b"\x1B\x61\x02")  # Right alignment
    else:  # Default to left alignment
        epson._raw(b"\x1B\x61\x00")  # Left alignment

    if indent > 0:
        # Set the left margin (indent) in characters
        epson._raw(b"\x1B\x42" + bytes([indent]))


def print_text(text):
    epson._raw(text.encode("utf-8") + b"\n")


# Test cases
set_text_alignment("start", 0)
print_text("starts-here")

set_text_alignment("start", 2)
print_text("starts-here")

set_text_alignment("start", 4)
print_text("starts-here")

set_text_alignment("start", 6)
print_text("starts-here")

set_text_alignment("start", 8)
print_text("starts-here")
# Cut the paper
epson.cut()

# Close the connection
epson.close()
