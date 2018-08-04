from kivy.app import App
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button


#Label:
#                    text: 'Insert the word that has to be added to the dictionary\\nN.B. \\n   1) if you want to add more then one word, use the semicolon (;) as separator;\\n   2) all the whitespaces and new lines will be deleted during the parsing of the words.'
#                    font_size: 18
#                TextInput:
#                    size_hint: 0.8, .5
#                    multiline: True,
#                    font_size: 18

Builder.load_string("""

<TweetCheckerScreen>:
    boxes: _boxes
    AnchorLayout:
        anchor_x: 'center'
        anchor_y: 'top'
        ScreenManager:
            size_hint: 1, .8
            id: _screen_manager
            Screen:
                name: 'screen1'
                BoxLayout: 
                    orientation: 'vertical'
                    padding: 50
                    id: _boxes 
        Button:
            size_hint: 1, .9
            text: 'Add a word to the dictionary'
            on_press:
                root.manager.transition.direction = 'left'
                root.manager.current = 'dict'

<DictionatyScreen>:
    boxes: _boxes
    AnchorLayout:
        anchor_x: 'center'
        anchor_y: 'top'
        ScreenManager:
            size_hint: 1, .8
            id: _screen_manager
            Screen:
                name: 'screen1'
                BoxLayout: 
                    orientation: 'vertical'
                    padding: 50
                    id: _boxes 
        Button:
            size_hint: 1, .1
            text: 'Check a tweet'
            on_press:
                root.manager.transition.direction = 'right'
                root.manager.current = 'tweet'

""")


class TweetCheckerScreen(Screen):
    def __init__(self, **kwargs):
        super(TweetCheckerScreen, self).__init__(**kwargs)
        bx1 = BoxLayout(orientation='horizontal')
        bx2 = BoxLayout(orientation='horizontal')
        bx3 = BoxLayout(orientation='horizontal')
        bx4 = BoxLayout(orientation='horizontal')
        bx5 = BoxLayout(orientation='horizontal')

        header_message = Label(text='Insert the tweet in the following box:', font_size=26)
        bx1.add_widget(header_message)

        tweetbox = TextInput(multiline=True, font_size=16)
        tweetbox.hint_text = "Insert the tweet that has to be checked here"
        bx2.add_widget(tweetbox)

        corrected_tweet = TextInput(multiline=True, font_size=16)
        corrected_tweet.hint_text = "the corrected tweet will appear here"
        corrected_tweet.readonly = True
        bx3.add_widget(corrected_tweet)


        button_check_tweet = Button(text = "Check tweet")
        bx4.add_widget(button_check_tweet)

        self.boxes.add_widget(bx1)
        self.boxes.add_widget(bx2)
        self.boxes.add_widget(bx3)
        self.boxes.add_widget(bx4)

class DictionatyScreen(Screen):
    def __init__(self, **kwargs):
        super(DictionatyScreen, self).__init__(**kwargs)
        bx1 = BoxLayout(orientation='horizontal')
        bx2 = BoxLayout(orientation='horizontal')
        bx3 = BoxLayout(orientation='horizontal')
        bx4 = BoxLayout(orientation='horizontal')

        header_message = Label(text='Insert the tweet in the following box:', font_size=26)
        bx1.add_widget(header_message)

        tweetbox = TextInput(multiline=True, font_size=16)
        tweetbox.hint_text = "Insert the tweet that has to be checked here"
        bx2.add_widget(tweetbox)

        corrected_tweet = TextInput(multiline=True, font_size=16)
        corrected_tweet.hint_text = "the corrected tweet will appear here"
        corrected_tweet.readonly = True
        bx3.add_widget(corrected_tweet)


        button_check_tweet = Button(text = "Check tweet")
        bx4.add_widget(button_check_tweet)

        self.boxes.add_widget(bx1)
        self.boxes.add_widget(bx2)
        self.boxes.add_widget(bx3)
        self.boxes.add_widget(bx4)

sm = ScreenManager()
sm.add_widget(TweetCheckerScreen(name='tweet'))
sm.add_widget(DictionatyScreen(name='dict'))


class TestApp(App):
    def build(self):
        return sm

if __name__ == '__main__':
    TestApp().run()