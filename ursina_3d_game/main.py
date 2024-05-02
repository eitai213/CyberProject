from ursina import *
import map
import player
import gun

app = Ursina()

map.Map()
player.Player()

a = gun.Gun()



def update():
    a.update()




app.run()
