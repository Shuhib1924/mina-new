from PIL import Image

name = "./ch.jpg"


def resize():
    img = Image.open(name)
    img.thumbnail((200, 200), Image.LANCZOS)
    img.save(f"{name}.png")
    img.show()


if __name__ == "__main__":
    resize()
