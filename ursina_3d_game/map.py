from ursina import *
from ursina.shaders import lit_with_shadows_shader


class Map:
    def __init__(self):
        Entity.default_shader = lit_with_shadows_shader

        self.map = Entity(model = 'cube', scale=(100, 1, 100), texture='brick', texture_scale=(4, 4), collider='box')


        sun = DirectionalLight()
        sun.look_at(Vec3(1, -1, -1))
        Sky()
