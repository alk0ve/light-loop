import pyglet
from pathlib import Path
pyglet.resource.path = [str(Path(__file__).resolve().parent)]
pyglet.resource.reindex()


def load_image(name: str):
    image = pyglet.resource.image(name)
    image.anchor_x = image.width // 2
    image.anchor_y = image.height // 2
    return image
