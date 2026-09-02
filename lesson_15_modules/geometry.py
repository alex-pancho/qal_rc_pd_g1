__all__ = ["Circle", "Rectangle"]   # тільки ці імена є публічними


class Circle:
    def __init__(self, radius: float):
        self.radius = radius


class Rectangle:
    def __init__(self, w: float, h: float):
        self.w, self.h = w, h


class _InternalHelper:      # приватний: починається з _
    pass