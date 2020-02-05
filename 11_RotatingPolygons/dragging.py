from kivy.uix.scatter import Scatter
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.app import App
from kivy.uix.scatterlayout import ScatterLayout
from kivy.graphics.transformation import Matrix
###########
from kivy.uix.bubble import Bubble, BubbleButton
from kivy.graphics import Triangle
from math import cos, sin, radians
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
toch = 300.0, 36.87, 400.0, 53.13, 500.0, 90.0


class MyScatterLayout(ScatterLayout):
    move_lock = False
    scale_lock_left = False
    scale_lock_right = False
    scale_lock_top = False
    scale_lock_bottom = False

    def on_touch_up(self, touch):
        self.move_lock = False
        self.scale_lock_left = False
        self.scale_lock_right = False
        self.scale_lock_top = False
        self.scale_lock_bottom = False
        if touch.grab_current is self:
            touch.ungrab(self)
            x = self.pos[0] / 10
            x = round(x, 0)
            x = x * 10
            y = self.pos[1] / 10
            y = round(y, 0)
            y = y * 10
            self.pos = x, y
            return super(MyScatterLayout, self).on_touch_up(touch)

    """def transform_with_touch(self, touch):
        changed = False
        x = self.bbox[0][0]
        y = self.bbox[0][1]
        width = self.bbox[1][0]
        height = self.bbox[1][1]
        mid_x = x + width / 2
        mid_y = y + height / 2
        inner_width = width * 0.5
        inner_height = height * 0.5
        left = mid_x - (inner_width / 2)
        right = mid_x + (inner_width / 2)
        top = mid_y + (inner_height / 2)
        bottom = mid_y - (inner_height / 2)

            # just do a simple one finger drag
        if len(self._touches) == self.translation_touches:
            # _last_touch_pos has last pos in correct parent space,
            # just like incoming touch
            dx = (touch.x - self._last_touch_pos[touch][0]) \
                 * self.do_translation_x
            dy = (touch.y - self._last_touch_pos[touch][1]) \
                 * self.do_translation_y
            dx = dx / self.translation_touches
            dy = dy / self.translation_touches
            if (touch.x > left and touch.x < right and touch.y < top and touch.y > bottom or self.move_lock) and not self.scale_lock_left and not self.scale_lock_right and not self.scale_lock_top and not self.scale_lock_bottom:
                self.move_lock = True
                self.apply_transform(Matrix().translate(dx, dy, 0))
                changed = True

        change_x = touch.x - self.prev_x
        change_y = touch.y - self.prev_y
        anchor_sign = 1
        sign = 1
        if abs(change_x) >= 9 and not self.move_lock and not self.scale_lock_top and not self.scale_lock_bottom:
            if change_x < 0:
                sign = -1
            if (touch.x < left or self.scale_lock_left) and not self.scale_lock_right:
                self.scale_lock_left = True
                self.pos = (self.pos[0] + (sign * 10), self.pos[1])
                anchor_sign = -1
            elif (touch.x > right or self.scale_lock_right) and not self.scale_lock_left:
                self.scale_lock_right = True
            self.size[0] = self.size[0] + (sign * anchor_sign * 10)
            self.prev_x = touch.x
            changed = True
        if abs(change_y) >= 9 and not self.move_lock and not self.scale_lock_left and not self.scale_lock_right:
            if change_y < 0:
                sign = -1
            if (touch.y > top or self.scale_lock_top) and not self.scale_lock_bottom:
                self.scale_lock_top = True
            elif (touch.y < bottom or self.scale_lock_bottom) and not self.scale_lock_top:
                self.scale_lock_bottom = True
                self.pos = (self.pos[0], self.pos[1] + (sign * 10))
                anchor_sign = -1
            self.size[1] = self.size[1] + (sign * anchor_sign * 10)
            self.prev_y = touch.y
            changed = True
        return changed"""

    def on_touch_down(self, touch):
        x, y = touch.x, touch.y
        self.prev_x = touch.x
        self.prev_y = touch.y
        # if the touch isnt on the widget we do nothing
        if not self.collide_widget(mpw):
            return False

        if not self.do_collide_after_children:
            if not self.collide_point(x, y):
                return False

        # let the child widgets handle the event if they want
        touch.push()
        touch.apply_transform_2d(self.to_local)
        if super(Scatter, self).on_touch_down(touch):
            # ensure children don't have to do it themselves
            if 'multitouch_sim' in touch.profile:
                touch.multitouch_sim = True
            touch.pop()
            self._bring_to_front(touch)
            return True
        touch.pop()

        # if our child didn't do anything, and if we don't have any active
        # interaction control, then don't accept the touch.
        if not self.do_translation_x and \
                not self.do_translation_y and \
                not self.do_rotation and \
                not self.do_scale:
            return False

        if self.do_collide_after_children:
            if not self.collide_point(x, y):
                return False

        if 'multitouch_sim' in touch.profile:
            touch.multitouch_sim = True
        # grab the touch so we get all it later move events for sure
        self._bring_to_front(touch)
        touch.grab(self)
        self._touches.append(touch)
        self._last_touch_pos[touch] = touch.pos

        return True


class MyButton(Button):
    def on_touch_down(self, touch):
        return False


class MyFloatLayout(FloatLayout):
    pass


class ccp(Bubble):
    def __init__(self, **kwargs):
        super(ccp, self).__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (80, 30)
        self.add_widget(BubbleButton(text='Data'))
        self.add_widget(BubbleButton(text='Delete'))


class Polygon(Triangle):
    def __init__(self, data, **kwargs):
        super(Polygon, self).__init__(**kwargs)
        l, h = 0, 0  # po_x po_y
        toch = (l, h, l+data[2], h, l+cos(radians(data[5]))*data[0], h+sin(radians(data[5]))*data[0])
        self.points = l, h, l+data[2], h, l+cos(radians(data[5]))*data[0], h+sin(radians(data[5]))*data[0]


class MyPolygonWidget(Widget):
    triangle = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(MyPolygonWidget, self).__init__(**kwargs)
        self.add_widget(Button(text='1234', on_press=lambda a: print(1234)))
        #with self.canvas:
            #self.triangle = Polygon(toch)

    def on_touch_down(self, touch):
        #self.show_bubble()
        return

    def show_bubble(self, *l):
        if not hasattr(self, 'bubb'):
            self.bubb = bubb = ccp()
            self.add_widget(bubb)
        else:
            values = ('left_top', 'left_mid', 'left_bottom', 'top_left',
                      'top_mid', 'top_right', 'right_top', 'right_mid',
                      'right_bottom', 'bottom_left', 'bottom_mid', 'bottom_right')
            index = values.index(self.bubb.arrow_pos)
            self.bubb.arrow_pos = values[(index + 1) % len(values)]


class ScatterApp(App):
    def build(self):
        f = MyFloatLayout()
        s2 = MyScatterLayout(do_rotation=False, size=(toch[2], toch[0]*sin(radians(toch[5]))), size_hint=(None, None))
        global mpw
        mpw = MyPolygonWidget()
        s2.add_widget(mpw)
        f.add_widget(s2)
        return f


ScatterApp().run()
