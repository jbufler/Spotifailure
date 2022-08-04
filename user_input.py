from functools import partial
from threading import Thread
from anyio import open_process

import yfinance as yfinance
from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.storage.jsonstore import JsonStore
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.video import Video

from user_data import* 
from Evaluation import * 
from Setup_file import * 


class WelcomeView(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 1
        self.size_hint = (0.6, 0.7)
        self.pos_hint = {
            'center_x': 0.5,
            'center_y': 0.5
        }

        self.add_widget(Image(source='external_data/logo.png'))
        self.greeting = Label(text='What is your name?',
                              font_size=18,
                              color='#33cccc')
        self.add_widget(self.greeting)
        self.user = TextInput(multiline=False,
                              padding_y=(20, 20),
                              size_hint=(1, 0.5)
                              )

        self.add_widget(self.user)
        self.entrance_button = Button(text='START',
                                      size_hint=(1, 0.5),
                                      bold=True,
                                      background_color='#33cccc',
                                      background_normal='')
        self.entrance_button.bind(on_press=self.entrance_button_behaviour)
        self.add_widget(self.entrance_button)

    def entrance_button_behaviour(self, *args):
        self.greeting.text = f'Welcome {self.user.text}!'
        Clock.schedule_once(self.switch_to_next_view, 2)

    def switch_to_next_view(self, *args):
        app.screen_manager.current = 'stockView'
    


class StockView(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 1
        self.size_hint = (0.6, 0.7)
        self.pos_hint = {
            'center_x': 0.5,
            'center_y': 0.5
        }

        self.greeting = Label(text='Wanna check out some fancy functionalities?',
                              font_size=18,
                              color='#33cccc')
        self.add_widget(self.greeting)
 
        # 1st row
        self.yes_button = Button(text ='YES PLEASE')
        self.no_button = Button(text ='No, thank you. I was just looking around. \n              Just play a random song.',
                                size_hint=(1, 0.5),
                                bold=True,
                                background_color='#33cccc',
                                background_normal='')
        self.no_button.bind(on_press=self.no_button_behavior)
        self.yes_button.bind(on_press=self.yes_button_behavior)
        self.add_widget(self.no_button)
        self.add_widget(self.yes_button)

    def yes_button_behavior(self, *args):
        Clock.schedule_once(self.switch_to_next_view, 2) 

    def no_button_behavior(self, *args): 
        self.greeting.text = "Never gonna say goodbye..."
        self.video = Video(source='external_data/NGGUU.mp4', play = True)
        self.video.options = {'eos': 'loop'}
        self.clear_widgets([self.yes_button, self.no_button])
        self.add_widget(self.video)
        self.video.allow_stretch=True
            
    def switch_to_next_view(self, *args):
        app.screen_manager.current = "optionView"



class OptionView(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 1
        self.size_hint = (0.6, 0.7)
        self.pos_hint = {
            'center_x': 0.5,
            'center_y': 0.5
        }

        self.feature = "danceability"

        self.greeting = Label(text='Choose one :D!',
                              font_size=18,
                              color='#33cccc')
        self.add_widget(self.greeting)

        self.popularity = Button(text ='Is my taste of music unique or mainstream?')
        self.popularity.bind(on_press=self.button_behavior)
        self.matplotlib = Button(text= 'Which music personality are u? danceable/acousticness/... ')
        self.matplotlib.bind(on_press=self.button_behavior)
        self.seaborn_heatmap = Button(text= 'Which of your music personality types may correlate?')
        self.seaborn_heatmap.bind(on_press=self.button_behavior)
        self.artist_chart = Button(text= 'Who are my favourite artists?')
        self.artist_chart.bind(on_press = self.button_behavior)
        self.danceable = Button(text="Challenge a friend: Whose playlist is more danceabel / energetic / ...?")
        self.danceable.bind(on_press=self.button_behavior)
        self.playlist_generation = Button(text= 'What about creating a playlist with a friend?')
        self.playlist_generation.bind(on_press=self.button_behavior)
    
        self.add_widget(self.popularity)
        self.add_widget(self.matplotlib)
        self.add_widget(self.seaborn_heatmap)
        self.add_widget(self.artist_chart)
        self.add_widget(self.danceable)
        self.add_widget(self.playlist_generation)

        self.button_dict = {1: self.popularity.text, 2: self.matplotlib.text, 3:self.seaborn_heatmap.text, 4:self.artist_chart.text, 5:self.danceable.text, 6:self.playlist_generation.text}

        self.user = Setup(c_id, c_secret, redirect)
        self.sp = self.user.getSpotifyInstance()
        self.df1 = self.user.top_genre_extraction()

        self.user2 = Setup(c_id2, c_secret2, redirect2)
        self.sp2 = self.user2.getSpotifyInstance()
        self.df2 = self.user2.top_genre_extraction()

    def back_to_menu(self, *args):
        Clock.schedule_once(self.switch_to_menu, 3) 

    
    def button_behavior(self, button, *args): 
        #self.greeting.text = button.text
        #self.clear_widgets([self.popularity, self.matplotlib, self.seaborn_heatmap, self.artist_chart, self.danceable, self.playlist_generation])
        for id, text in self.button_dict.items():
            if text == button.text:
                number = id


        # back to menu + quit button 
        match number: 
            # popularity 
            case 1:
                g = GridLayout(cols = 1,
                size_hint = (0.6, 0.7),
                pos_hint = {
                    'center_x': 0.5,
                    'center_y': 0.5
                })
                
                screen = Screen(name="popularity")
                screen.add_widget(g)
                app.screen_manager.add_widget(screen)
                Clock.schedule_once(self.switch_to_next_view, 2) 
                
                s =  popularity(self.df1)
                #self.greeting.text += s
                result = Label(text=s,
                                    font_size=18,
                                    color='#33cccc')
                g.add_widget(result)
                but = Button(text="BACK TO MAIN MENU", size_hint =(.5, .1))
                but.bind(on_press=self.back_to_menu)
                g.add_widget(but)

            # matplotlib 
            case 2:
                g = GridLayout(cols = 1,
                size_hint = (0.6, 0.7),
                pos_hint = {
                    'center_x': 0.5,
                    'center_y': 0.5
                })
                screen = Screen(name="matplotlib")
                screen.add_widget(g)
                app.screen_manager.add_widget(screen)
                Clock.schedule_once(self.switch_view, 2) 
                matplotlib(self.df1)
                but = Button(text="BACK TO MAIN MENU", size_hint =(.5, .1))
                but.bind(on_press=self.back_to_menu)
                g.add_widget(but)
            
            # seaborn heatmap
            case 3: 
                g = GridLayout(cols = 1,
                size_hint = (0.6, 0.7),
                pos_hint = {
                    'center_x': 0.5,
                    'center_y': 0.5
                })
                screen = Screen(name="heatmap")
                screen.add_widget(g)
                app.screen_manager.add_widget(screen)
                Clock.schedule_once(self.switch_to_heatmap, 2) 
                seaborn_heatmap(self.df1)
                but = Button(text="BACK TO MAIN MENU", size_hint =(.5, .1))
                but.bind(on_press=self.back_to_menu)
                g.add_widget(but)

            # artist 
            case 4: 
                g = GridLayout(cols = 1,
                size_hint = (0.6, 0.7),
                pos_hint = {
                    'center_x': 0.5,
                    'center_y': 0.5
                })
                screen = Screen(name="artist")
                screen.add_widget(g)
                app.screen_manager.add_widget(screen)
                Clock.schedule_once(self.switch_to_artist, 2) 
                artist_chart(self.df1)
                but = Button(text="BACK TO MAIN MENU", size_hint =(.5, .1))
                but.bind(on_press=self.back_to_menu)
                g.add_widget(but)

            # challenge a friend 
            case 5:

                g = GridLayout(cols = 1,
                size_hint = (0.6, 0.7),
                pos_hint = {
                    'center_x': 0.5,
                    'center_y': 0.5
                })
                screen = Screen(name="challenge")
                screen.add_widget(g)
                app.screen_manager.add_widget(screen)
                Clock.schedule_once(self.switch_to_challenge, 2) 

                question = Label(text='Which feature do you want to check?',
                              font_size=18,
                              color='#33cccc')
                g.add_widget(question)
                # user input: playlist id, feature (feature mit buttons lösen )
                # Adding the text input
                
                # buttons FEATURES 
                danceability = Button(text ='danceability')
                valence = Button(text ='valence')
                liveness = Button(text='liveness')
                loudness = Button(text="loudness")
                energy = Button(text="energy")
                tempo = Button(text="tempo")

                danceability.bind(on_press=lambda x:self.input_flush(danceability))
                valence.bind(on_press=lambda x:self.input_flush(valence))
                liveness.bind(on_press=lambda x:self.input_flush(liveness))
                loudness.bind(on_press=lambda x:self.input_flush(loudness))
                energy.bind(on_press=lambda x:self.input_flush(energy))
                tempo.bind(on_press=lambda x:self.input_flush(tempo))

                g.add_widget(danceability)
                g.add_widget(valence)
                g.add_widget(liveness)
                g.add_widget(loudness)
                g.add_widget(energy)
                g.add_widget(tempo)

                # second view 
                g2 = GridLayout(cols = 1,
                size_hint = (0.6, 0.7),
                pos_hint = {
                    'center_x': 0.5,
                    'center_y': 0.5
                })
                screen = Screen(name="challenge2")
                screen.add_widget(g2)
                app.screen_manager.add_widget(screen)
                

                if from_ == 2: 
                    # only for user 2
                    output = feature(self.sp2, 0, self.feature, playlist_id, playlist_id2)

                elif from_ == 1: 
                    output =feature(self.sp, 0, self.feature, playlist_id, playlist_id2)

                elif from_ == 0: 
                    output = feature(self.sp, self.sp2, self.feature, playlist_id, playlist_id2)

                output_ = Label(text=output,
                              font_size=18,
                              color='#33cccc')
                g2.add_widget(output_)

                
                but = Button(text="BACK TO MAIN MENU", size_hint =(.5, .1))
                but.bind(on_press=self.back_to_menu)
                g2.add_widget(but)
            


            # playlist collaboration
            case 6: 
                playlist_generation(self.df1, self.df2, username, username2, self.sp, self.sp2)
    
    
    def input_flush(self, button, *args): 
        Clock.schedule_once(self.switch_to_challenge2, 2)
        self.feature = button.text

    def switch_to_challenge2(self,*args): 
        app.screen_manager.current = "challenge2"

    def switch_to_challenge(self, *args): 
        app.screen_manager.current = "challenge"

    def switch_to_artist(self, *args): 
        app.screen_manager.current = "artist"

    def switch_to_heatmap(self, *args): 
        app.screen_manager.current = "heatmap"

    def switch_view(self, *args): 
        app.screen_manager.current = "matplotlib"

    def switch_to_next_view(self, *args):
        app.screen_manager.current = "popularity"
    
    def switch_to_menu(self, *args): 
        app.screen_manager.current = "optionView"
        
        




class MyApp(App):
    def build(self):
        self.screen_manager = ScreenManager()
        self.welcome_view = WelcomeView()
        screen = Screen(name='welcomeView')
        screen.add_widget(self.welcome_view)
        self.screen_manager.add_widget(screen)

        self.stock_view = StockView()
        screen = Screen(name='stockView')
        screen.add_widget(self.stock_view)
        self.screen_manager.add_widget(screen)


        self.option_view = OptionView()
        screen = Screen(name="optionView")
        screen.add_widget(self.option_view)
        self.screen_manager.add_widget(screen)


        if(self.screen_manager.current_screen == "endView"): 
            self.end_view.play_video()
        

        return self.screen_manager


if __name__ == '__main__':
    app = MyApp()
    app.run()