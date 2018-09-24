import webbrowser, os
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from training import CustomHMM, TweetChecker

Builder.load_string("""

<TweetCheckerScreen>:
    boxes: _boxes
    AnchorLayout:
        anchor_x: 'center'
        anchor_y: 'bottom'
        BoxLayout: 
            orientation: 'vertical'
            padding: 50
            id: _boxes     
        BoxLayout: 
            Button:
                size_hint: 0.5, .1
                text: 'Add a word to the dictionary'
                on_press:
                    root.manager.transition.direction = 'left'
                    root.manager.current = 'dict'
            Button:
                size_hint: 0.25, .1
                text: 'Options'
                on_press:
                    root.manager.transition.direction = 'down'
                    root.manager.current = 'opt'
            Button:
                size_hint: 0.25, .1
                text: 'More information'
                on_press:
                    root.manager.transition.direction = 'up'
                    root.manager.current = 'info'
        
<DictionatyScreen>:
    boxes: _boxes
    AnchorLayout:
        anchor_x: 'center'
        anchor_y: 'bottom'
        BoxLayout: 
            orientation: 'vertical'
            padding: 50
            id: _boxes     
        BoxLayout: 
            Button:
                size_hint: 0.5, .1
                text: 'Check a tweet'
                on_press:
                    root.manager.transition.direction = 'right'
                    root.manager.current = 'tweet'
            Button:
                size_hint: 0.25, .1
                text: 'Options'
                on_press:
                    root.manager.transition.direction = 'down'
                    root.manager.current = 'opt'
            Button:
                size_hint: 0.25, .1
                text: 'More information'
                on_press:
                    root.manager.transition.direction = 'up'
                    root.manager.current = 'info'
                    
<Options>
    boxes: _boxes
    AnchorLayout:
        anchor_x: 'center'
        anchor_y: 'bottom'
        BoxLayout: 
            orientation: 'vertical'
            padding: 50
            id: _boxes     
        BoxLayout: 
            Button:
                size_hint: 0.375, .1
                text: 'Check a tweet'
                on_press:
                    root.manager.transition.direction = 'up'
                    root.manager.current = 'tweet'
            Button:
                size_hint: 0.375, .1
                text: 'Add a word to the dictionary'
                on_press:
                    root.manager.transition.direction = 'up'
                    root.manager.current = 'dict'
            Button:
                size_hint: 0.25, .1
                text: 'More information'
                on_press:
                    root.manager.transition.direction = 'up'
                    root.manager.current = 'info'

<Information>
    boxes: _boxes
    AnchorLayout:
        anchor_x: 'center'
        anchor_y: 'bottom'
        BoxLayout: 
            orientation: 'vertical'
            padding: 50
            id: _boxes     
        BoxLayout: 
            Button:
                size_hint: 0.375, .1
                text: 'Check a tweet'
                on_press:
                    root.manager.transition.direction = 'down'
                    root.manager.current = 'tweet'
            Button:
                size_hint: 0.375, .1
                text: 'Add a word to the dictionary'
                on_press:
                    root.manager.transition.direction = 'down'
                    root.manager.current = 'dict'
            Button:
                size_hint: 0.25, .1
                text: 'Options'
                on_press:
                    root.manager.transition.direction = 'down'
                    root.manager.current = 'opt'

""")

selected_hmm = "HMM_20"
available_hmm = ('HMM_10', 'HMM_20', 'HMM_30')

class TweetCheckerScreen(Screen):
    tweet_text = TextInput(multiline=True, font_size=16, markup=True)
    corrected_tweet = TextInput(multiline=True, font_size=16)


    def __init__(self, **kwargs):
        super(TweetCheckerScreen, self).__init__(**kwargs)
        bx1 = BoxLayout(orientation='horizontal')
        tweetbox = BoxLayout(orientation='horizontal')
        correctionbox = BoxLayout(orientation='horizontal')
        bx4 = BoxLayout(orientation='horizontal')

        header_message = Label(text='Insert the tweet in the following box:', font_size=26)
        bx1.add_widget(header_message)

        self.tweet_text.hint_text = "Insert the tweet that has to be checked here"
        tweetbox.add_widget(self.tweet_text)

        self.corrected_tweet.hint_text = "the corrected tweet will appear here"
        self.corrected_tweet.readonly = True
        correctionbox.add_widget(self.corrected_tweet)


        button_check_tweet = Button(
            text = "Check tweet",
            font_size=20,
            on_press=lambda a: self.check()
        )
        bx4.add_widget(button_check_tweet)

        self.boxes.add_widget(bx1)
        self.boxes.add_widget(tweetbox)
        self.boxes.add_widget(correctionbox)
        self.boxes.add_widget(bx4)
        self.boxes.add_widget(BoxLayout(orientation='horizontal'))
        self.boxes.add_widget(BoxLayout(orientation='horizontal'))

    def check(self):
        global selected_hmm
        model = CustomHMM.load("./best_hmms/" + selected_hmm + "/")

        self.corrected_tweet.text = TweetChecker.dull_check(self.tweet_text.text, model)
        text = TweetChecker.parse(self.tweet_text.text)
        new_text = ""
        for word in str(self.tweet_text.text).split(" "):
            if TweetChecker.parse(word) in text and not(word + " " in model.vocabulary):
                new_text += "error(" + word + ") "
            else:
                new_text += word + " "
        self.tweet_text.text = new_text

        #self.corrected_tweet.text = TweetChecker.sentense_check(self.tweet_text.text, model)


class DictionatyScreen(Screen):
    wordsbox = TextInput(multiline=True, font_size=16)
    ack_box = Label(text="", font_size=20)

    def __init__(self, **kwargs):
        super(DictionatyScreen, self).__init__(**kwargs)
        bx1 = BoxLayout(orientation='horizontal')
        bx2 = BoxLayout(orientation='horizontal')
        bx3 = BoxLayout(orientation='horizontal')
        bx4 = BoxLayout(orientation='horizontal')

        message = "Insert the word that has to be added to the dictionary" \
                  "\nKeep in mind that: \n" \
                  "   1) if you want to add more then one word, " \
                  "use the semicolon (;) as separator;\n" \
                  "   2) all the whitespaces and new lines will be deleted " \
                  "during the parsing of the words."
        header_message = Label(text = message, font_size=20)
        bx1.add_widget(header_message)

        self.wordsbox.hint_text = "Insert the word/s here (Ex. hello;Mark;identifier;...)"
        bx2.add_widget(self.wordsbox)

        button_check_tweet = Button(
            text = "Add word/s",
            font_size=20,
            on_press = lambda a: self.add()
        )
        bx3.add_widget(button_check_tweet)

        bx4.add_widget(self.ack_box)

        self.boxes.add_widget(bx1)
        self.boxes.add_widget(BoxLayout(orientation='horizontal'))
        self.boxes.add_widget(bx2)
        self.boxes.add_widget(bx3)
        self.boxes.add_widget(bx4)
        self.boxes.add_widget(BoxLayout(orientation='horizontal'))

    def add(self):
        global available_hmm
        words = str(self.wordsbox.text).replace("\n", "").replace(" ", "").split(";")

        for hmm in available_hmm:
            with open("./best_hmms/" + hmm + "/vocabulary.txt", "a") as voc:
                for word in words:
                    voc.write(word + "\n")

        self.wordsbox.text = ""
        self.ack_box.text = "The following words have been added:\n" + str(words)

class CustomSpinner(Spinner):

    def __init__(self, **kwargs):
        super(CustomSpinner, self).__init__(**kwargs)

    def _on_dropdown_select(self, instance, data, *largs):
        self.text = data
        global selected_hmm
        selected_hmm = data

class Options(Screen):
    def __init__(self, **kwargs):
        super(Options, self).__init__(**kwargs)
        global available_hmm

        bx1 = BoxLayout(orientation='horizontal')

        message = "Choose the HMM that you would like to use:"
        header_message = Label(text=message, font_size=20)
        bx1.add_widget(header_message)

        spinner = CustomSpinner(
            # default value shown
            text='HMM_20',
            # available values
            values=available_hmm,
            # just for positioning in our example
            size_hint=(None, None),
            size=(200, 44),
            pos_hint={'center_x': .5, 'center_y': .5},
        )


        bx1.add_widget(spinner)

        self.boxes.add_widget(bx1)

#class UrlLink(Label):
#    def __init__(self, **kwargs):
#        super(UrlLink, self).__init__(**kwargs)

 #   def on_touch_down(self, touch):
 #       #webbrowser.open("https://www.linkedin.com/in/umberto-azadi-26b431135/")
 #       os.system("start \"\" https://www.linkedin.com/in/umberto-azadi-26b431135/")


class Link(Label):
    def __init__(self, type, **kwargs):
        super(Link, self).__init__(**kwargs)
        self.type = type

    def on_touch_down(self, touch):
        if self.type == "pdf":
            webbrowser.open(r'file:' + os.path.realpath("./../docs/Report.pdf"))
        if self.type == "url":
            webbrowser.open("https://www.linkedin.com/in/umberto-azadi-26b431135/")



class Information(Screen):
    def __init__(self, **kwargs):
        super(Information, self).__init__(**kwargs)
        bx1 = BoxLayout(orientation='horizontal')
        bx2 = BoxLayout(orientation='horizontal')
        bx3 = BoxLayout(orientation='horizontal')


        message = "For any further information about this project please see: "
        header_message = Label(text=message, font_size=18)
        #link = Link("pdf", text=pdf_name, font_size=20, color=[0, 0.5, 1, 1])
        link = Button(
            text="Report.pdf",
            font_size=20,
            on_press=lambda a:webbrowser.open(r'file:' + os.path.realpath("./../docs/Report.pdf")),
            size_hint=(0.5, 1)
        )

        message1 = "For any further information about the developer: "
        header_message1 = Label(text=message1, font_size=18)
        link1 = Button(
            text="Umberto Azadi",
            font_size=20,
            on_press=lambda a:webbrowser.open("https://www.linkedin.com/in/umberto-azadi-26b431135/"),
            size_hint=(0.5, 1)
        )

        github = Button(
            text="GitHub Repository",
            font_size=20,
            on_press=lambda a: webbrowser.open("https://github.com/uazadi/OMIT"),
            size_hint=(0.5, 1)
        )


        bx1.add_widget(header_message)
        bx1.add_widget(link)
        bx2.add_widget(header_message1)
        bx2.add_widget(link1)
        bx3.add_widget(github)

        self.boxes.add_widget(BoxLayout(orientation='horizontal'))
        self.boxes.add_widget(bx1)
        self.boxes.add_widget(BoxLayout(orientation='horizontal'))
        self.boxes.add_widget(bx2)
        self.boxes.add_widget(BoxLayout(orientation='horizontal'))
        self.boxes.add_widget(bx3)
        self.boxes.add_widget(BoxLayout(orientation='horizontal'))

sm = ScreenManager()
sm.add_widget(TweetCheckerScreen(name='tweet'))
sm.add_widget(DictionatyScreen(name='dict'))
sm.add_widget(Options(name='opt'))
sm.add_widget(Information(name='info'))


class TestApp(App):
    def build(self):
        self.title = "Tweet checker"
        return sm

if __name__ == '__main__':
    TestApp().run()