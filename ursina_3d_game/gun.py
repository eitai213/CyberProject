from ursina import *


class Gun:
    def __init__(self):

        self.gun = Entity(model='cube', parent=camera, position=(.5, -.25, .25), scale=(.3, .2, 1), origin_z=-.5,
                     color=color.red, on_cooldown=False)
        self.gun.muzzle_flash = Entity(parent=self.gun, z=1, world_scale=.5, model='quad', color=color.yellow, enabled=False)

        shootables_parent = Entity()
        mouse.traverse_target = shootables_parent


    def update(self):
        if held_keys['left mouse']:
            self.shoot()

    def shoot(self):
        if not self.gun.on_cooldown:
            #print('shoot')
            self.gun.on_cooldown = True
            self.gun.muzzle_flash.enabled = True
            from ursina.prefabs.ursfx import ursfx
            ursfx([(0.0, 0.0), (0.1, 0.9), (0.15, 0.75), (0.3, 0.14), (0.6, 0.0)], volume=0.5, wave='noise',
            pitch=random.uniform(-13, -12), pitch_change=-12, speed=3.0)
            invoke(self.gun.muzzle_flash.disable, delay=.05)
            invoke(setattr, self.gun, 'on_cooldown', False, delay=.15)
            if mouse.hovered_entity and hasattr(mouse.hovered_entity, 'hp'):
                mouse.hovered_entity.hp -= 10
                mouse.hovered_entity.blink(color.red)

