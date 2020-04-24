#!/usr/bin/env python3
# -*- coding: utf-8 -*-

print("a")

#import for setting up database
from libdw import pyrebase

#Database Set-Up
projectid = "anshiqadwgame"
dburl = "https://" + projectid + ".firebaseio.com"
authdomain = projectid+ ".firebaseapp.com"
apikey = "AIzaSyCNIj9n7yY_5se0MzkVtl-O4ljDPmWKHLg"
email = "anshi.2018@gmail.com"
password = "123456"

config = {
    "apiKey": apikey,
    "authDomain":authdomain,
    "databaseURL": dburl,
}
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
user = auth.sign_in_with_email_and_password(email, password)
db = firebase.database()

#------------------------------------------------------------------------------------------------------------------   
#set new key-value pair to test Firebase
root = db.child ("bob").set(3.345, user['idToken'])
#------------------------------------------------------------------------------------------------------------------   
#Define function to create new user node
def new_user(name, category):
    users_node = db.child('users')
    users_node.set({
    'Player1': {
        'category_chosen': str(category),
        'user_name': str(name)
    }})
    
#------------------------------------------------------------------------------------------------------------------   

#State machines (Set up Streak State Machine to compute awarded points)
from libdw import sm
class StreakSm(sm.SM):
    start_state = 0
    def get_next_values(self, state, input):
        if state == 0:
            if input == 'W':
                next_state = 0
                output = int(0)
            elif input == 'C' :
                next_state = 1
                output = int(1)

        if state == 1 :
            if input == 'W':
                next_state = 0
                output = int(0)
            elif input == 'C' :
                next_state = 2
                output = int(2)

        if state == 2 :
            if input == 'W':
                next_state = 0
                output = int(0)
            elif input == 'C' :
                next_state = 2
                output = int(2)
        return next_state, output

#------------------------------------------------------------------------------------------------------------------   
#Define function to Process animals txt file
def process_words(category):
    if str(category) == 'Animals':
        file_name = 'An_List_Avec_blanks'
    elif category == 'Cities':
        file_name = 'City_List.txt'
    elif category == 'DW Fun':
        file_name = 'An_List_Avec_blanks'
    full_word_list =[]
    word_list_blanks =[]
    f = open(str(file_name),"r")
    for line in f:
        l=line.strip()
        ls = l.split()
        if (len(ls) != 0):
            if (ls[0].isalnum() == True):
                full_word_list.append(ls[0])
            else:
                word_list_blanks.append(ls[0]) 
    f.close
    return full_word_list, word_list_blanks
#------------------------------------------------------------------------------------------------------------------   
#Define function to check answer
def check_ans(their_ans, chosen_an):
    if their_ans == chosen_an:
        check = 'C'
        print ('Yes!')    
    else:
        check = 'W'
        print ("No!")
    return check

#------------------------------------------------------------------------------------------------------------------   
import random
#Define fn to generate random numbers that are not repeated
def gen_ran_num(end_range,used_num_list):
    while True:
        ran_num = random.randint(0, end_range)
        if ran_num not in used_num_list:
            break
    return ran_num

#------------------------------------------------------------------------------------------------------------------   

# imports kivy library
import kivy
# include the latest version of the kivy
# import required classes
from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.text import LabelBase
from kivy.uix.textinput import TextInput
from kivy.properties import ObjectProperty
from kivy.uix.gridlayout import GridLayout
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock


kivy.require('1.11.1')

#Register fonts using LabelBase. For Bold etc specifiy with True/False in Kv
LabelBase.register(name = "Lato", 
                   fn_regular= 'Lato-Regular.ttf', 
                   fn_italic='Lato-HeavyItalic.ttf')
LabelBase.register(name = "DIN_Alt", 
                   fn_regular= 'DIN Alternate Bold.ttf')
LabelBase.register(name = "DIN_Cond", 
                   fn_regular= 'DIN Condensed Bold.ttf')
  
#----------------------------------------------------------------------------------
# Declare all screens and colours in rgba tuples

c_beige = (0.909, 0.815, 0.662, 1)
c_brown = (0.717, 0.686, 0.639, 1)
c_green = (0.756, 0.854, 0.839,0.8)
c_white = (0.960, 0.980, 0.980,1)
c_lBlue = (0.674, 0.819, 0.913,1)
c_DBlue= (0.427, 0.572, 0.607,1)

#Background Window color
Window.clearcolor = c_green

#-------------------------------------------------------------------------------------
#Design all screens.

Builder.load_string("""                    
<StartScreen>:
    BoxLayout:
        orientation: 'vertical'
        spacing: 10
        padding: 20
    
        Label:
            text: 'GUESS THE WORD'
            font_name: "DIN_Alt"
            size_hint_y: 0.5
            font_size: 60
            color:0,0,0, 1
            background_color: 0.674, 0.819, 0.913,1
        
        GridLayout:
            cols: 2
            size_hint_y: 1
        
            Label:
                width: 10
                text: 'Step 1. Enter Username'
                font_name: "DIN_Alt"
                font_size: 20
                color: 0,0,0,1

            Label:
                width: 10
                text: 'Step 2. Select A Category:'
                font_name: "DIN_Alt"
                font_size: 20
                color: 0,0,0,1
                
                
            TextInput: 
                text: ''
                id: nameInput
                font_size: 18
            
            Button:
                id: animal_Cat
                text: 'Animals'
                font_name: "DIN_Alt"
                font_size: 24
                background_color: 0.427, 0.572, 0.607,1
                on_press: root.enterAnimals()
            
            Label:
                width: 10
                color: 0,0,0,1                                       
           
            Button:
                id: cities_Cat                                            
                text: 'Cities'
                font_name: "DIN_Alt"
                font_size: 24
                background_color: 0.427, 0.572, 0.607,1
                on_press: root.enterCities()
           
            Label:
                width: 10
                color: 0,0,0,1
                
            
            Button:                                            
                id: dW_Cat
                text: 'DW Fun'
                font_name: "DIN_Alt"
                font_size: 24
                background_color:0.427, 0.572, 0.607,1
                on_press: root.enterDW()
            
        
        Button:
            text: 'Step 3. Press ENTER to play'
            background_color: 0,0,0,0.8
            size_hint_x: 1
            size_hint_y: 0.3
            font_name: "DIN_Alt"
            font_size: 20
            on_press: 
                root.manager.current = 'Instruct'
                       
<InstructScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: 20
        spacing: 15
        
        Label:
            text: 'Instructions for GUESS THE WORD'
            underline: True
            font_name: "DIN_Alt"
            font_size: 30
            halign: 'center'

            
        
        Label:
            text: 'Blanks in the word represent missing letters. Guess the word, type in your answer & Press GUESS. Type Skip if you are unsure. Once you are on a streak, with two or more consecutive correct answers, you will win 2 points for each answer! Each game has 10 words. At the end of the game, restart to play again and beat your previous record!'
            font_name: "DIN_Cond"
            font_size: 28
            text_size: self.size
            halign: 'center'
            valign: 'top'
            
        Button:
            text: "Got it, lets play!"
            background_color: 0,0,0,0.8
            size_hint_x: 1
            size_hint_y: 0.3
            font_name: "DIN_Alt"
            font_size: 30
            on_press: 
                root.manager.current = 'Game'
            
            
<GameScreen>:
    BoxLayout:
        orientation: 'vertical'
        spacing: 5
        padding: 20
        
        Label:
            text: 'GUESS THE WORD'
            font_name: "Lato"
            font_size: 14
            size_hint_y: 0.1
            color: 0.427, 0.572, 0.607,1
       
        Label:
            text: 'LOADING...'
            size_hint_y: 0.2
            id: gameHeader
            font_name: "DIN_Alt"
            font_size: 24
            color: 0,0, 0, 1
       
        Label:
            id: question
            text: '_ _ I G E _'
            size_hint_y: 0.4
            font_name: "Lato"
            font_size: 40
            color: 0,0,0, 1
            
        Label:
            text: 'Write SKIP if unsure'
            size_hint_y: 0.2
            font_name: "DIN_Cond"
            italic: True
            font_size: 22
            color: 0,0,0,1
        
        GridLayout: 
            id:game_grid
            cols: 2
            padding: 10
            size_hint_y: 1
            
            TextInput:
                id:answer
                text: ''
                font_name: "Lato"
                font_size: 20   
       
            Button:
                text: 'GUESS!'
                font_size: 20
                font_name: 'DIN_Alt'
                background_color: 0.427, 0.572, 0.607,0.9
                on_press: root.now_check_player()
                on_press: root.now_up_counter()
                on_release: root.now_gen_newword()
                on_release: root.clear_input_text()
        
                
            Label: 
                id: indicate_Correct
                text: "   "
                width: 10
                font_name: "DIN_Cond"
                font_size: 20
                color: 0,0,0,0.7
            
            Label:
                id:player_points
                text: 'Points: 0'
                font_name: "DIN_Cond"
                font_size: 30
                color: 0,0,0,1
                
            Label:
                id: player_streak
                text: 'Streak: '
                font_name: "DIN_Cond"
                font_size: 24
                color: 0,0,0,1
            
            Label: 
                width: 10
                color: 0,0,0,1      
            
                
        Button:
            text: 'End Game'
            size_hint_y: 0.2
            font_name: "DIN_Alt"
            font_size: 20
            background_color:  0.427, 0.572, 0.607,0.9
            on_press: 
                root.reset_counter_usednum()
                root.manager.transition.direction = 'left'
                root.manager.current = 'End'


<EndScreen>:
    BoxLayout:
        Button:
            text: 'RESTART'
            font_name: "DIN_Alt"
            font_size: 30
            background_color:  0.427, 0.572, 0.607,0.9
            on_press: 
                root.manager.transition.direction = 'left'
                root.manager.current = 'Instruct'

""")
#--------------------------------------------------------------------
# Create the app classes
    #StartScreen
class StartScreen(Screen):
    nameInput = ObjectProperty(None)
    animal_Cat = ObjectProperty(None)
    cities_Cat = ObjectProperty(None)
    dW_Cat = ObjectProperty(None) 
    def enterAnimals(self):
        #make fn enter user name and catoegory in the firebase. 
        self.name = str(self.ids.nameInput.text)
        self.category = str(self.ids.animal_Cat.text)
        new_user(self.name, self.category)
    def enterCities(self):
        #make fn enter user name and catoegory in the firebase. 
        self.name = str(self.ids.nameInput.text)
        self.category = str(self.ids.cities_Cat.text)
        new_user(self.name, self.category)
    def enterDW(self):
        #make fn enter user name and catoegory in the firebase. 
        self.name = str(self.ids.nameInput.text)
        self.category = str(self.ids.dW_Cat.text)
        new_user(self.name, self.category)
    pass

class InstructScreen(Screen):
    pass
#--------------------------------------------------------------------------------------------------------------------------
#Game Screen
class GameScreen(Screen):
    def __init__(self, **kwargs):
        super(GameScreen, self).__init__(**kwargs)
        Clock.schedule_once(self.change_gameHeader,0.5)
        Clock.schedule_once(self.play_game,0.5)
    #define widgets from screen as screen class properties
    question = ObjectProperty(None)
    answer = ObjectProperty(None)
    gameHeader = ObjectProperty(None)
    player_points =ObjectProperty(None)
    player_streak =ObjectProperty(None)
    indicate_Correct = ObjectProperty(None)
    category = db.child("users").child("Player1").child("category_chosen").get().val()
    
    def change_gameHeader(self,dt):
        if (db.child("users").child("Player1").child("category_chosen").get().val()) == 'Animals':
            self.ids.gameHeader.text = "Which Animal Is This?"
        elif (db.child("users").child("Player1").child("category_chosen").get().val()) == 'Cities':
            self.ids.gameHeader.text = "Which City Is This?"
        elif (db.child("users").child("Player1").child("category_chosen").get().val()) == 'DW FUN':
            self.ids.gameHeader.text = "Which DW term Is This?"       
                
                #also, assign StreakSm's output at this point to new variable, called 'addition'
                
                #update counter and points
            
    def play_game(self,dt):        
       #initialize empty varibale
        self.counter = 0
        self.points = 0
        self.used_num_list=[]
        self.addition = 0
        self.check = str(0)

        #define what category in gamescreen class and process txt file
        self.category = str(self.category)
        self.full_word_list, self.word_list_blanks = process_words(self.category)
        self.total_words = int(len(self.full_word_list))
        self.end_range = self.total_words - 1 
        
        ##start SM, new SM class instance called 'go' and 
        #do one step of get_next_value method in the 'go' SM class instance 
        self.go = StreakSm() 
        self.go.start()
    
        #Igenerate first ran num and choose first question and answer
        self.ran_num = gen_ran_num(self.end_range,self.used_num_list)
        self.chosen_ques = str(self.word_list_blanks[self.ran_num])
        self.chosen_ans = str(self.full_word_list[self.ran_num])
        print ("self.chosen_ans v1: " + self.chosen_ans) 
        print ("self.chosen_ques v1: " + self.chosen_ques) 
        
        #convert all to uppercase to avoid cae-sensitivity
        self.chosen_ques = self.chosen_ques.upper()
        self.chosen_ans = self.chosen_ans.upper()
        print ("self.chosen_ans v2: " + self.chosen_ans) 
        print ("self.chosen_ques v2: " + self.chosen_ques) 
       
        #change text of 'question' label the chosen quesiton
        self.ids.question.text= self.chosen_ques
    
    def now_check_player(self):
        #capitalise player's answer text
        self.ids.answer.text = str(self.ids.answer.text)
        self.ids.answer.text = self.ids.answer.text.upper()
        print ("self.ids.answer.text: "+ self.ids.answer.text)
        print ("self.chosen_ans: " + self.chosen_ans)
        
        # now_check_player's ans
        check = check_ans(self.ids.answer.text, self.chosen_ans)
        self.check = check
        print ("self.check v1: " + str(self.check))
       
        # now_calculate_addition to points for this round via 'go' statemachine
        addition = self.go.step(self.check)
        self.addition=addition
        
        #sum up total points and display on screen
        self.points += self.addition
        print ("self.points: " + str(self.points))
        self.ids.player_points.text = "Points: " + str(self.points)
        
        #now_update_streak:
        if self.addition == 0:
            self.ids.player_streak.text = "Streak: N0 :("
            self.ids.indicate_Correct.text = "Wrong! +0"
        elif self.addition == 1:
            self.ids.player_streak.text = "Streak: Almost..."
            self.ids.indicate_Correct.text = "Correct! +1"
        elif self.addition == 2:
            self.ids.player_streak.text = "Streak: YES!"
            self.ids.indicate_Correct.text = "Correct! +2"
        
        #now_update_used number list
        self.used_num_list.append(self.ran_num)
        print ("self.used_num_list: ", self.used_num_list)
        
    def now_up_counter(self):
        self.counter = self.counter+1
        print ("self.counter: " + str(self.counter))
        return self.counter

    #generate new word for next round. 
    '''this is done on_release and not on_press because when done on_press, the 
    chosen answer changes before the right answer can be checked''' 
    def now_gen_newword(self):
        if self.counter < 10:
            self.ran_num = gen_ran_num(self.end_range,self.used_num_list)
            self.chosen_ques = str(self.word_list_blanks[self.ran_num])
            self.chosen_ans = str(self.full_word_list[self.ran_num])
            self.chosen_ques = self.chosen_ques.upper()
            self.chosen_ans = self.chosen_ans.upper()
            self.ids.question.text= self.chosen_ques
        else:
            self.ids.question.text = "Congrats, "+str(db.child("users").child("Player1").child("user_name").get().val())+"! You have won "+str(self.points)+" points!"
        
    def clear_input_text(self):
         self.ids.answer.text = ''        
        
    def reset_counter_usednum(self):
        self.counter = 0
        self.points = 0
        self.ids.player_points.text = "Points: 0"
        self.used_num_list = []
        #change qn display also, otherwise the qn text will remain as congrats
        self.ran_num = gen_ran_num(self.end_range,self.used_num_list)
        self.chosen_ques = str(self.word_list_blanks[self.ran_num])
        self.chosen_ans = str(self.full_word_list[self.ran_num])
        self.chosen_ques = self.chosen_ques.upper()
        self.chosen_ans = self.chosen_ans.upper()
        self.ids.question.text= self.chosen_ques
        #return state to 0 and streak text to no
        self.go.start()
        self.ids.player_streak.text = "Streak: "
        self.ids.indicate_Correct.text = " "
        
    pass

#--------------------------------------------------------------------
#End Screen
class EndScreen(Screen):
    pass
#--------------------------------------------------------------------
#Add screens to Screen Manager
screen_man = ScreenManager()
screen_man.add_widget(StartScreen(name='Start'))
screen_man.add_widget(InstructScreen(name='Instruct'))
screen_man.add_widget(GameScreen(name='Game'))
screen_man.add_widget(EndScreen(name='End'))

class AnshiApp(App):
    def build(self):
        return screen_man
#--------------------------------------------------------------------
#Run App
if __name__ == '__main__':
    AnshiApp().run()

