# -*- coding: utf-8 -*-
"""
Created on Tue Sep  7 23:44:54 2021

@author: neeraj
"""

# Notes:
# - Making a Kivy app for android requires MacOS or Linux since buildozer isn't available for windows. A VM running these
#   works too.
# - 

# Main Game

from kivy.app import App
from kivy.core.window import Window
# from kivy.uix.widget import Widget
from kivy.uix.scatter import Scatter
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout


class MineField(GridLayout):
    
    def __init__(self, **kwargs):
        super(MineField, self).__init__(**kwargs)
        self.cols = 10
        self.rows = 10
        # self.add_widget(Label(text='O', background_color = (1,0,0,1)))
        # self.add_widget(Label(text='O', background_color = (0.8,0.8,0.8,1)))


class MinesweeperApp(App):
    
    def build(self):
        # return Label(text = "Minesweeper Game - v1")
        m = MineField()
        
        for i in range(100):
            m.add_widget(Button(background_color = (1,1,1,1)))
        # b = BoxLayout(orientation='vertical')
        # t = TextInput(font_size = 28,
                      # size_hint_y = None,
                      # height = 40,
                      # text = 'default')
        # f = FloatLayout()
        # s = Scatter()
        # l = Label(text = "Random Word",
                  # font_size = 28)
        # # return Button(text = "Start Button",
                      # # background_color = (0,1,0,1),
                      # # font_size = 28)
        
        # t.bind(text = l.setter('text')) #bind the setter function for the text field of the label.
        
        # f.add_widget(s)
        # s.add_widget(l)
        
        # b.add_widget(t)
        # b.add_widget(f)
        return m
        
    def quitApp(self):
        Window.close()    


if __name__ == '__main__':
    print("Starting game...")
    MinesweeperApp().run()
    MinesweeperApp().quitApp()
    