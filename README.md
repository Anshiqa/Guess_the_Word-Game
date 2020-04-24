# Guess The Word Game
2020 Digital World FInal Exam Programming Assignment:
Develop a Game 
<br><hr><br>
Anshiqa Agrawal, Singapore Universoty of Technology and Design
## Introduction
This game was designed and developed for the Digital World course in my first year undergad studies at SUTD as a module final exam assignment. As the name implies, the player guesses a word, comprising of blanks to represent some missing letters, to win points. On a streak (2 or more correct in a row), the player wins double points for each correct answer.
<br><br>
The game is written using Python language and the GUI is created through Kivy.
### How To Use
Please download the following files from the repo to use:
1. Main Python File: Anshiqa_Guess_Word_MiniGame.py
2. Text Files: 
     * City_List.txt
     * An_List_Avec_blanks
     * DW_term_list.txt
3. Fonts:
    * DIN Alternate Bold.ttf
    * DIN Condensed Bold.ttf
    * Lato-HeavyItalic.ttf
    * Lato-Regular.ttf
 
### How to Play
To play the game, the player first enters a 'Username' and selects a category. The 'Username' and category are stored in a firebase database, to be called upon later. This is done so that these variables can be easily used across screens.
<br><br>
There are 3 categories: Animals, Cities and DW Fun (Digital World)
<br><br>
'Animals' is the easiest while 'Cities' is quite difficult.
<br><br>
When playing, the player is shown a word with blanks like, 'C_T'. The blank represents a missing letter in this case, 'A. The player types the answer 'cat' in the input box and presses the 'GUESS' button. If the answer is not known, the player can write 'skip' and press the guess button. **Note that the answer is not case sensitive.**
<br><br>
For each correct answer, the player gets one point. When he gets 2 or more consecutively correct answer, player goes on a 'streak' and wins 2 points for each correct answer. At the end of 10 words, the game ends and the player is shown his final points. Then, he clicks the end game button and can restart if desired. 
#### Game Design Decisions
1. The game was first written as a complete, wokring text-based game on python and then the GUI was created using Kivy as a self-challenge and to make it more interactive. 
2. There are 4 screen classes in the Kivy code: StartScreen, InstructScreen, GameScreen, EndScreen
3. Firebase is used to store the player's USERNAME and CATEGORY selected. This is because in Kivy, these variables are collected from an 'textinput' widget and a 'button' widget respectively from within the StartScreen. I found it easier to access these variables from other screen classes by storing them and then calling them from Firebase, compared to trying to make them global variables inside the code. 
4. The code is designed such that the in a single game, the animals are never repeated, until the game is restarted. This uses the function defined as gen_ran_num.
<br><br>

    def gen_ran_num(end_range,used_num_list):
        while True:
            ran_num = random.randint(0, end_range)
            if ran_num not in used_num_list:
                break
        return ran_num
        
        
5. Everytime after the player presses 'Guess' button, the input text is cleared automatically. This also prevents any mistakes in self-clearing the text input

6. Streak State Machine
    States: 
    No Streak - 0
    Almost Streak - 1
    Streak - 2
    
    The ouput represents number of points gained.
    
    | Current State | Input | Next State | Output |
    | --- | ----------- |--- | ----------- |
    | 0 | C | 0 | 0 |
    | 0 | W |1 | 1 |
    | 1 | C | 0 | 0 |
    | 1 | W |2 | 1 |
    | 2 | C | 0 | 0 |
    | 2 | W |2 | 2 |
    
7. After 10 words are played, the game ends. When the player clicks the 'End Game' button, it does the following:
    * Resets the counter for number of words 
    * Clears the used random number list 
    * Restarts player points variable to 0 and changes points display text to 'Points: 0' 
    * Sicne the same label widget is used to display the question word and the "Congrats" text, the end button also changes the "congrats" text back into a new question word, not seen by player.
    * Swipes to next screen 
    
    Then, on the next screen, the RESTART button simply brings the player back to the InstructScreen to enter the GameScreen via the button. 
    
  
##### Technologies 
* Python
* Firebase Database
* Kivy Lang for GUI


Watch a demo: https://youtu.be/hCsKSCgUcIY
