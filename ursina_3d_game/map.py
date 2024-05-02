from ursina import *
from ursina.shaders import lit_with_shadows_shader


class Map:
    def __init__(self):
        Entity.default_shader = lit_with_shadows_shader

        self.map = Entity(model = 'plane', scale=64, texture='brick', texture_scale=(4, 4), collider='box')

        for i in range(16):
            Entity(model='cube', origin_y=-.5, scale=2, texture='brick', texture_scale=(1, 2),
                   x=random.uniform(-8, 8),
                   z=random.uniform(-8, 8) + 8,
                   collider='box',
                   scale_y=random.uniform(2, 3),
                   color=color.hsv(0, 0, random.uniform(.9, 1))
                   )
        sun = DirectionalLight()
        sun.look_at(Vec3(1, -1, -1))
        Sky()
