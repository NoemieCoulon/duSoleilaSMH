# coding: utf-8
import numpy as np
import matplotlib.pyplot as plt

class Roof:
    def __init__(self, name, pdl, roof_m2, potential):
        self.name = name
        self.pdl = pdl
        self.roof_m2 = roof_m2
        self.potential = potential

    def get_info(self):
        print(f"Bâtiment: {self.name}")
        print(f"Pdl: {self.pdl}")