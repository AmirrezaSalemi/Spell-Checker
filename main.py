from operator import itemgetter
import string
from tkinter import *
from tkinter import ttk
from tkinter import colorchooser
import Levenshtein

corrects = [] # a list for store correct words and best word for replacing with wrong words.
corrects_list = [] # a list that store 10 off best words for replacing with each wrong word.
wrongs = 0 # a counter for counting number of wrong words if their count is more than 0 then user can edit texts.


def correction(): # a definition for correcting all the wrong words.
    text.delete('1.0', END) # Delete all words in user Textboxs
    for string in corrects: # add best word for replacing of each mistake word and correct words to TextBox.
        text.insert(END, string + ' ') # insert correct words one by one to end of User TextBox.


def correct_end(): # a definition that user can correct only the last wrong answer of User TextBox.
    def close_second_window(): # a definition that user choose correct word or add wrong word to dictionary and then the second window closed. 
        if combo_box.get() != 'new correct word': # a condition if user didn't want to add wrong word to dictionary.
            if combo_box.get() in dic: # a condition that check if word the user choosed its in dictionary then the word added to corrects list.
                corrects[i] = combo_box.get() # add correct word to corrrects list.
        else: # a condition for when user wanna add wrong word to dictionary.
            with open('Dictionary.txt', 'a', encoding='utf-8') as filew: # open dictionary file as filew in writer mode.
                filew.write('\n'+corrects[i]) # write word in dictionary. 
            filew.close() # close dictionary file.
            dic[corrects[i]] = 0 # add word to dictionary of python.
        
        text.delete('1.0', END) # delete all words in User TextBox.
        for words in corrects: # add words with edited last wrong word to user TextBox.
                text.insert(END, words + ' ')
        window1.destroy() # destrot the top window.
        window.deiconify() # reaccess to main window.
    def close(): # a definition for closing top window.
        window1.destroy() # destrot the top window.
        window.deiconify() # reaccess to main window.
        
    corrects = [] # a list for store words that the last wrong word edited to correct word.
    if len(corrects_list) > 0 and wrongs > 0: # a condition that if number of wrong answers are more than or equal 1.
        window1 = Toplevel(window) # creat a top level window for user to choose correct word.
        window1.geometry('200x200') # set top window defult size in 200 * 200.
        window1.grab_set() # The widget grabs all events for the top window.
        window1.focus_set() # the user can just use this window.
        window1.protocol("WM_DELETE_WINDOW", close) # if user use crose in top the top window should close.
        base1 = text.get("1.0", "end-1c").lower() # get user TExtBox words and convert it to lower case because our dictionary works with lower cases.
        base = ''.join([c for c in base1 if c not in string.punctuation]).split() # remove Punctuation marks and split it to words
        reverse = list(reversed(base)) # reverse list of words to get last wrong word.
        corrects.clear() # clear list of correct words and get it ready for previouse word with new correctword instead of last wrong word.
        corrects = list(text.get("1.0", END).split()) # get user TextBox words and add it to a list.
        i = -1
        for strings in reverse: # Move over the inverted list to find the last wrong word.
            if strings not in dic: # a condition that hapend if word isn't in dictionary 
                Date = Label(window1, text=strings, fg="red") # creat a lebel for showing wrong word.
                Asterick = Label(window1, text=' change with: ', fg="black") 
                Date.grid(row=0, column=0) #
                Asterick.grid(row=0, column=1)
                
                combo_box = ttk.Combobox(window1, values=corrects_list[i] + list(['new correct word'])) # a comboBox for showing correct words for editing wrong word and a new word option for adding wrong word to dictionary.
                combo_box.grid(row=1, column=0, columnspan=2) # add ComboBox to top window.
                combo_box.current(0) # at first comboBox show the best word that can replace with wrong word.
                close_button = Button(window1, text="correct", command=close_second_window) # a button that after click on it the wrong word change with word selected from comboBox and the top window closed.
                close_button.grid(row=3, column=0, columnspan=2) # add button to top window.
                window1.grid_columnconfigure(0, weight=1)
                window1.grid_columnconfigure(1, weight=1)
                break
            i += -1


def checker(): # a definition for check words and highlighting mistakes.
    global wrongs # use global variable of wrongs.
    sentence = text.get("1.0", "end-1c").lower() # get words in user TextBox and make them lowerCase because our dictionary use lower words. 
    words = ''.join([c for c in sentence if c not in string.punctuation]).split() # remove punctuation of string in TextBox and split it word by word.
    fail_text.delete('1.0', END) # make Mistake TextBox empty to add new mistakes( if we have mistake).
    distance_text.delete('1.0', END) # make recomend words TextBox empty for recommend new words for new word mistakes( if we have new mistake.).
    corrects.clear() # clear correct words list because we wana check words again and add the correc of each word to this list.
    corrects_list.clear() # clear list of 10 best words that we can replace with wrongs because we wana check words again and recommend new lists. 
    wrongs = 0 # set number of wrong words 0 befor check from begin to end of Text.
    for word in words: # a loop that check if word in dictionary add it to user TextBox in black and if not in dictionary add it to text in reed and send it to edit distance definition to get recommended words for editting text.
        if word in dic: # a condition that if word in dictionary works.
            corrects.append(word) #because word in dictionary add it to list of correct words in text.
            corrects_list.append([word])
            fail_text.insert(END, word + ' ', "black")
        else: # a condition that if word isnt in dictionary it works.
            wrongs += 1 # because word isn't in dictionary number of wrong words aget increase by 1.
            fail_text.insert(END, word + ' ', "red")
            correct(word) # call correct definition to get best words that we can replace with wrong word.
    distance_text.after(100, checker) # recall checker function each 100ms to detect wrongs in momment(real time mistake founder).


def correct(word):
    lis = get_list(word, dictionary) # a list that sorted in order of best words we can replace with wrong word. 
    corrects.append(lis[0]) # add first and best word that we can recommend.
    corrects_list.append(lis) # 10 best words that we can recommend.
    distance_text.insert(END, word, 'red') # in this three line we recommend best words.
    distance_text.insert(END, ' -> ', 'black')
    distance_text.insert(END, str(lis) + '\n', 'blue')


def get_list(word, dictionary):
    for word2 in dic:
        dictionary[word2] = Levenshtein.distance(word, word2) # call our edit distance algorithm.
    dictionary = dict(sorted(dictionary.items(), key=itemgetter(1))) # sort our dictionary by lowest distance.
    lis = []
    counter = 0
    for value in dictionary: # a loop for add 10 best words to recommend list.
        if counter != 10:
            lis.append(value)
            counter += 1
        else:
            break
    return lis


def make_empty(dictionary): # a definition that make values in dictionary -1.
    for word in dic:
        dictionary[word] = -1


window = Tk() # create a Tk window as main Window of application.
window.title('Spell Mistake Founder') # set a title for my main window.
window.geometry('1080x500') # set a defult size for each time the app runs.
window.resizable(height=False, width=False) # make app unresizable. (its optional i use for my own.)

with open('Dictionary.txt', 'r', encoding='utf-8') as file: # open my dictionary with name file.
    txt = file.read() # read my dictionary that opend in previous line.
dic = { # a dictionary for setting my words in it.

}
spl = txt.split('\n') # split my word in dictionary and set it in spl list.
for word in spl: # read words in spl list and put it in dictionary.
    dic[word] = 0
dictionary = { # A dictionary to store the distances we count.

}
make_empty(dictionary) # At begin all words should have 0 distance.

inp = Label(window, text="InputText: ", foreground='green')
inp.pack() # line 158 its about a label that show "Input Text".
text = Text(window, width=1080, height=0, wrap='none') # create a TextBox for get input from User.
text.pack(pady=(5, 50), padx=(50, 50)) # Pack the TextBox.

mistake = Label(window, text='Spell Mistake Check: ', foreground='blue')
mistake.pack() # line 162 its about a label that show "Spell Mistake Check".
fail_text = Text(window, width=1080, height=5, wrap='none') # create a TextBox for show mistakes in red and corrects in black.
fail_text.tag_configure('black', foreground='black') # set black tag for correct words.
fail_text.tag_configure('red', foreground='red') # set red tag for wrong Words.
fail_text.pack(pady=(5, 50), padx=(50, 50)) # Pack the Mistakes TextBox.

words = Label(window, text='Correction Word: ', foreground='violet')
words.pack() # line 168 its about a label that show "Correct Words".
distance_text = Text(window, width=1080, height=10, wrap='none') # A TexBox for offering correct words for mistakes.
distance_text.tag_configure('black', foreground='black') # set black tag for  this "->" symbol. 😂
distance_text.tag_configure('blue', foreground='blue') # set blue tag for offered words.
distance_text.tag_configure('red', foreground='red') # set red tag for wrong word.
distance_text.pack(pady=(5, 5), padx=(50, 50)) # Pack the offer TextBox.

checker() # Call a function that search in input text for find wrong words and correct words.

button = Button(window, text='correct All', foreground='green', command=correction) # Create a Button that after clicked correct all wrong words with their lowest far distance word. 
button.pack() # Pack correct all words Button.
button2 = Button(window, text='correct last one', foreground='green', command=correct_end) # Creat a Button that after clicked oppen a new window whith a ComboBox that 10 of best words that user can replace with wrong words are in it and user can choose them or add the wrong word to dictionary.
button2.pack() # Pack correct last wrong word Button.
   
def background():
    color = colorchooser.askcolor()
    if color[1]:
        window.config(background=color[1])
        inp.config(background=color[1])
        words.config(background=color[1])
        mistake.config(background=color[1])


def textboxback():
    color = colorchooser.askcolor()
    if color[1]:
        text.config(background=color[1])
        fail_text.config(background=color[1])
        distance_text.config(background=color[1])

def textboxfront():
    color = colorchooser.askcolor()
    if color[1]:
        text.config(fg=color[1])
        fail_text.config(fg=color[1])
        distance_text.config(fg=color[1])
    
    
menubar = Menu(window) # Creat a menubar.
view = Menu(menubar, tearoff=0)
view.add_command(label='BackGround Color', command=background)
view.add_command(label='TextBoxes BackGround color', command=textboxback)
view.add_command(label="Input TextBoxes Front Color", command=textboxfront)
menubar.add_cascade(label='Design', menu=view)
menubar.add_command(label='Exit', command=window.quit) # a menue option to close app.
window.config(menu=menubar) # set menubar for main window
mainloop() # a loop for showing main window.