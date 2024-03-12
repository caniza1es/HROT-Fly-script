from pymem import Pymem
from math import *
import keyboard


pm = Pymem("HROT.exe")


class Entity:
    def __init__(self, index):
        self.index = index
        self.health = index * 8 + 0x180F800
        self.x = index * 8 + 0x180F7DC
        self.y = index * 8 + 0x180F7E0
        self.z = index * 8 + 0x180F7E4

        if index == 0:
            self.dx = 0xDE68F8
            self.dy = 0xDE68FC
            self.dz = 0xDE6900
    
    def get_orientation(self):
        return [pm.read_float(self.dx), pm.read_float(self.dy),pm.read_float(self.dz)]

    def get_position(self):
        return [pm.read_float(self.x), pm.read_float(self.y), pm.read_float(self.z)]

    def set_position(self, pos):
        x, y, z = pos
        pm.write_float(self.x, x)
        pm.write_float(self.y, y)
        pm.write_float(self.z, z)


def magnitude(vec):
    return sqrt(sum(i**2 for i in vec))

def norm(vec):
    m = magnitude(vec)
    return [i/m for i in vec]



def fly(ply,s=0.01):
    dirvec = ply.get_orientation()
    posvec = ply.get_position()
    posvec = [posvec[i]+dirvec[i]*s for i in range(3)]
    ply.set_position(posvec)
    


player = Entity(0)


flying = False
s=0.03
while True:
    if keyboard.is_pressed("f"):
        flying = not flying
        posvec = player.get_position()
    if flying:
        dirvec = player.get_orientation()
        right_vec = [dirvec[2], 0, -dirvec[0]] 
        if keyboard.is_pressed("w"):
            posvec = [posvec[i]+dirvec[i]*s for i in range(3)]
        elif keyboard.is_pressed("s"):
            posvec = [posvec[i]-dirvec[i]*s for i in range(3)]
        elif keyboard.is_pressed("a"):
            posvec = [posvec[i] + right_vec[i] * s for i in range(3)]
        elif keyboard.is_pressed("d"):
            posvec = [posvec[i] - right_vec[i] * s for i in range(3)]
        elif keyboard.is_pressed("space"):
            posvec[1] += s
        elif keyboard.is_pressed("ctrl"):
            posvec[1] -= s

        player.set_position(posvec)      
               
        
        
