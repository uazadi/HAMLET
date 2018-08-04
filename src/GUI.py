from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivy.uix.button import Button
#from kivy.properties import ListProperty


class CustomBtn(Widget):
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.pressed = touch.pos
            # we consumed the touch. return False here to propagate
            # the touch further to the children.
            return True
        return super(CustomBtn, self).on_touch_down(touch)

    def on_pressed(self, instance, pos):
        print ('pressed at {pos}'.format(pos=pos))

class LoginScreen(GridLayout):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.cols = 1
        label = Label(text='Insert the tweet in the following box:', font_size=26)
        self.add_widget(label)
        self.username = TextInput(multiline=True)
        self.add_widget(self.username)
        self.button = Button(
            text = 'Check the tweet',
            font_size = 26,
            background_normal='',
            background_color=(1, 1, 1, 0.5)
        )
        #self.button.border = (40, 40, 40, 40)
        #self.button.background_normal = ''
        #self.button.background_color = (1, 1, 1, 0.5)
        #self.button.
        self.add_widget(self.button)

class MyApp(App):
    def build(self):
        return LoginScreen()

if __name__ == '__main__':
    MyApp().run()
