import pygame as PG
import math

HEIGHT = 600
WIDTH  = 800

class Layer(object):
    surf_image = None
    parallax_rate = 0
    hor_offset = 0
    ver_offset = 0

    def __init__(self, surf, p_rate):
        self.surf_image = surf
        self.parallax_rate = p_rate

    def scroll(self, hor_dir, ver_dir):
        self.hor_offset += hor_dir * self.parallax_rate

        #Vertical parallax remains a mystery to me. Probably needs its own rate.
        if ver_dir < 0:
            ver_dir = math.floor(ver_dir)
        elif ver_dir > 0:
            ver_dir = math.ceil(ver_dir)
        self.ver_offset += ver_dir

        #self.ver_offset += ver_dir #* self.parallax_rate

    def get_hor_offset(self):
        return self.hor_offset

    def get_ver_offset(self):
        return self.ver_offset

    def get_par_rate(self):
        return self.parallax_rate

    def get_surf_image(self):
        return self.surf_image
        
    def set_ver_offset(self, v_offset):
        self.ver_offset = v_offset
