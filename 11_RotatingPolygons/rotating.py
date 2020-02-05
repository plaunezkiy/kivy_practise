from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.graphics import Triangle, Line
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.graphics import Rotate
from math import cos, radians, sin

data = 300.0, 36.87, 400.0, 53.13, 500.0, 90.0


class Polygon(Triangle):
    def __init__(self, **kwargs):
        super(Polygon, self).__init__(**kwargs)
        l, h = 0, 0  # po_x po_y
        toch = (l, h, l + data[2], h, l + cos(radians(data[5])) * data[0], h + sin(radians(data[5])) * data[0])
        self.points = l, h, l + data[2], h, l + cos(radians(data[5])) * data[0], h + sin(radians(data[5])) * data[0]
        # self.on_press = lambda a: Rotate(angle=45)


class wid(Widget):
    triangle = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(wid, self).__init__(**kwargs)
        self.add_widget(Button(on_press=lambda a: print(self.pos)))
        with self.canvas.before:
            l, h = 0, 0  # po_x po_y
            data = 300.0, 36.87, 400.0, 53.13, 500.0, 90.0
            toch = (l, h, l + data[2], h, l + cos(radians(data[5])) * data[0], h + sin(radians(data[5])) * data[0])
            """Line(points=[l, h, l + data[2], h, l + cos(radians(data[5])) * data[0], h +
                         sin(radians(data[5])) * data[0]], width=20)"""
            # Rotate(angle=90, origin=self.center)


class Mama(App):
    def build(self):
        b = BoxLayout()
        b.add_widget(wid())
        b.add_widget(Button(text='1345678', on_press=lambda a: b.clear_widgets()))
        return b


Mama().run()
