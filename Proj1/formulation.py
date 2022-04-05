import math

import numpy as np
import matplotlib.pyplot as plt

import copy
import random
from math import exp

class Colaborator:
    def __init__(self, skill, name) -> None:
        self.name = name
        self.skill = skill

class Project:
    def __init__(self, duration, name, score, roles) -> None:
        self.name = name
        self.duration = duration
        self.score = score # score awarded for completing the project
        self.roles = roles # list of roles for contributors working on the project 
