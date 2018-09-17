import json
import sys
import time

class Data():
    def __init__(self):

        self.data = json.load(open("data.json"))
        self.word = self.getWord()

    def getData(self):
        return self.data

    def getWord(self):
        word = input("Enter a word to define: ")

        if(word.isalpha()):
            self.defineWord(word)
        else:
            print("Invalid Input")
            self.getWord()


    def defineWord(self,word):
        #lets get all the keys in the dictionary
        self.definition= self.data.keys()
        #when we have the keys we are going to check that the word is in the keys
        if(word in self.definition):
            definition = self.data[word]
            #check if there are multiple definitions
            if(len(definition)>1):
                count =0
                for items in(definition):
                    count = count+1
                    print("{}. {}".format(count,items))


            else:
                print("DEFINITION: {}".format(definition[0]))
                time.sleep(2)
                print("\n")


        else:
            print("The word is not in the dictionary\n")
            time.sleep(2)
            print("\n")

        time.sleep(1)
        self.menu()

    def menu(self):
        while(1):
            action =input("WHAT DO YOU WANT TO DO \n [1] - Look up another word \n [2] - Exit \n :")

            if(self.isValidNum(action) and int(action)<=2 and int(action)>0):
                if(int(action) ==1):
                    self.getWord()
                elif(int(action)==2):
                    sys.exit(0)
                break;
            else:
                print("Wrong input")
                time.sleep(1)


    def isValidNum(self,num):
        if(num.isdigit()):
            return True
        else:
            return False



#when we get the word

def main():

    data = Data()



main()
