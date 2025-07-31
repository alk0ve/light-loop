import pyglet


def load_image(name: str):
    image = pyglet.resource.image(name)
    image.anchor_x = image.width // 2
    image.anchor_y = image.height // 2
    return image
