import math


def distance_between(vector_a, vector_b):
    return math.sqrt((vector_a.x - vector_b.x)**2 + (vector_a.y - vector_b.y)**2)


class Vector2:
    "a poor man's vector class"

    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y
