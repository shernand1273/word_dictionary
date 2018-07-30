from tkinter import *
import tkinter.messagebox
import json
import difflib
from difflib import SequenceMatcher
from difflib import get_close_matches


font={"BOLD":'\033[1m'}

class Window:
    def __init__(self,master):
        mainFrame= Frame(master,pady=10,padx=10)#this is the mainframe holding the entry frame and result frame
        mainFrame.pack(fill=X)

        #This is the entry frame contained within the mainframe
        self.entry_frame=Frame(mainFrame)
        self.entry_frame.pack(fill=X)

        #create the label,entry, and button that goes in the entry_frame
        self.entry_label=Label(self.entry_frame,text="Word: ")
        self.entry_label.pack(side=LEFT)
        self.entry_box=Entry(self.entry_frame)
        self.entry_box.bind("<Return>",self.display)
        self.entry_box.pack(side=LEFT)
        self.entry_button=Button(self.entry_frame,text="Define",command= lambda: self.display(None))
        self.entry_button.pack(side=LEFT)

        #this is the result frame contained within the mainframe
        self.result_frame=Frame(mainFrame)
        self.result_frame.pack(fill=X,side=LEFT,padx=10,pady=10)



        self.text_label=Label(self.result_frame,text="",pady=20,wraplength=600,justify=LEFT)
        self.text_label.pack()


    #************Supporting Functions******************

    def display(self,arg):
        #get the entry input
        text= self.entry_box.get().lower()

        if(self.validated(text)):
            #now that the data is validated, call a function to deal read from the JSON file and find the word_definition
            self.findWord(text)
        self.entry_box.delete(0,END)

    #This function validates the input, ensures the user entered something, input doesn't have symbols/numbers, or longer than any word
    def validated(self,text_input):
        if(len(text_input)==0 or len(text_input)>50):
            if(len(text_input)==0):
                self.text_label.config(text="Enter something...")

            elif(len(text_input)>50):
                self.text_label.config(text="This is a really long word or jibberish...either way i don't have a definition for it")

        elif(text_input.isalpha()!=True):
            self.text_label.config(text="This is not a word...")

        return text_input

#this function will load the JSON file, extract the data, and find a match, if there is no match it will display "The word was not found"

    def findWord(self,theWord):

        try:
            data =json.load(open("data.json"))
            keySearch=data.keys()

            if(theWord in keySearch):
                definition = data[theWord]

                #we may have more than one definition so we are going to pass it to another definition to determine that
                self.printDefinition(definition,theWord)
            #this part will call a function that uses the difflib to make a suggestion on the word comparing similarity ratios
            if(theWord not in keySearch):
                self.suggestWord(data,keySearch,theWord)

        except FileNotFoundError:
            answer=tkinter.messagebox.showerror("Error","There was a problem opening the data file used by this program\nthe program will now close")
            if(answer=="ok"):
                exit()


    def suggestWord(self,fileData,fileKeys,wordToMatch):
        possibleWords=[]
        suggestion=" "


        for key in fileKeys:
            key=key.lower()
            ratio =SequenceMatcher(None,wordToMatch,key).ratio()*100
            ratio=int(ratio)

            if(ratio >= 80):
                possibleWords.append(key)

        #now that we have all the possible matches, suggest the words to the users
        #if there are multiple suggestions
        if(len(possibleWords)==1):
            #test that the suggestion is not going to be the same as the word, this has been happening with some searches
            if(possibleWords[0]==wordToMatch):
                suggestion="Nothing Found"
                self.text_label.config(text=suggestion)

            else:
                suggestion+= ("Did you mean " + possibleWords[0].title()+"?")
                self.text_label.config(text=suggestion)


        if(len(possibleWords)>1):
            if(wordToMatch in possibleWords):
                possibleWords.remove(wordToMatch)#This fixes the issue of the search word sometimes coming up in the suggestions

            #call the closestmatchFunction to find which one is the closest of the possibleWords
            self.closestMatch(wordToMatch,possibleWords)


        if(len(possibleWords)==0):
            suggestion="Nothing Found"
            self.text_label.config(text=suggestion)




    def closestMatch(self,theWord, possibilitiesList):
        bestMatch=get_close_matches(theWord,possibilitiesList)
        self.text_label.config(text="Did you mean "+bestMatch[0].title()+"?")


#This function is only called when there is a definition, and it breaks down the definition into numbered items if there are more than one
    def printDefinition(self,theDefinition,theWord):
        defined=theWord.upper()+"\n"

        if(len(theDefinition)==1):
            #create a buffer to store the definition

            defined += ("%s" % (theDefinition[0]))
            self.text_label.config(text=defined)
        if(len(theDefinition)>1):
            for i in range(len(theDefinition)):
                #build the string with all the definitions separated by new lines and numbered

                defined+=str(i+1)+". "+theDefinition[i]+"\n"
                self.text_label.config(text=defined)


root =Tk()
root.title("Dictionary")
window = Window(root)
root.mainloop()


#bug to fix - there are some words that are coming up in the suggestions that don't have definitions
