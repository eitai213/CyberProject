from ursina import *
import map
import player
import weapon


app = Ursina()

map.Map()
user = player.Player()
gun = weapon.Gun()



def update():
    gun.update()




app.run()
