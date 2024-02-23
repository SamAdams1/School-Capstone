import tkinter as tk
from tkinter import *
from tkinter import filedialog
from tkinter.filedialog import askopenfile
from tkinter import ttk
from tkinter import messagebox


root = tk.Tk()
root.geometry("450x300")  # Size of the window 
root.title('Create Your Own Quiz!')
myFont=('times', 18, 'bold')
LARGEFONT =("Verdana", 35)
uploadLabel = tk.Label(root,text='Upload File & read',width=30,font=myFont)  
uploadLabel.grid(row=1,column=2)
uploadButton = ttk.Button(root, text='Upload File', 
   width=20,command = lambda:upload_file())
uploadButton.grid(row=2,column=2)
csvFormatLbl = tk.Label(root, text='\nCsv Format:\n\nFill-in-the-blank: question,answer,fill-in-the-blank\n\nMultiple-choice: question,option1,option2,option3,option4,answer,multiple-choice')
csvFormatLbl.grid(row=4,column=2)

currentQuestion = 0
quizArray = []
score = 0
numQuestions= 0
numToFail = 0
numToPass = 0
questionsLeft = 0
wrongAnswers = 0

msgBoxNotShown = True

def upload_file():
    f_types = [('CSV files',"*.csv"),('All',"*.*")]
    file = filedialog.askopenfilename(filetypes=f_types)
    fob=open(file,'r')
    questionNum = 1
    for row in fob:
        question = row.replace("\n","").split(",")
        # print(question)

        quizArray.append(question)

    global numQuestions
    numQuestions = len(quizArray)
    global numToPass
    numToPass = numQuestions * 0.65
    global numToFail
    numToFail = (numQuestions - int(numToPass))
    # print(numToFail, int(numQuestions * 0.65), numQuestions - int(numQuestions * 0.65))
    root.destroy()
    createQuiz()
    

#shows the current question and choices
def showQuestion():
    #get the current question
    question = quizArray[currentQuestion]
    quesLabel.config(text=question[0])
    
    #Switch between multiple choice and fill in the blank questions
    #Show the answers on the buttons
    if question[-1] == "multiple-choice":
        textBox.pack_forget()
        submitButton.pack_forget()
        txtHintLbl.pack_forget()
        for i in range(4):
            answerBtns[i].pack(pady=10,ipadx=10,ipady=10)
            answerBtns[i].config(text=question[i+1], state='normal')#reset button state
            
        moveElementsBelow()
        
    else:
        textBox.pack(pady=10)
        submitButton.pack(pady=10,ipadx=10,ipady=10)
        txtHintLbl.pack(pady=10)
        submitButton.config(text="Submit", state='normal')
        for i in range(4):
            answerBtns[i].pack_forget()
            
        moveElementsBelow()
        

    #Clear feedback label and disable the next button
    feedbackLabel.config(text="")
    nextBtn.config(state="disabled")


#remove and add elements to make them below answer buttons
def moveElementsBelow():
    labels = [nextBtn,feedbackLabel,scoreLabel]
    for element in labels:
            element.pack_forget()
            element.pack(pady=10)


#helper function to only accept 1 decimal place floats, 0.1 not 0.11
def checkFloat(answer):
    #check if is float
    if answer.find(".") != -1:
        #only allow to tenths decimal place
        if len(answer.split(".")[1]) <= 1:
            return False
    
    #if not float return true
    return True



#check answer and see if it is right or wrong
def checkAnswer(choice):
    #get the current question
    question = quizArray[currentQuestion]
    if choice == "textbox":
        selectedAnswer = textBox.get("1.0", "end-1c").replace("\n","")
        if not selectedAnswer.isdigit() and checkFloat(selectedAnswer):
            return
    else:
        selectedAnswer = answerBtns[choice].cget("text")
    
    #check for fill in the blanks by seeing if the answer can be made into a float
    try:
        #check if response matches the correct answer
        if float(selectedAnswer) == float(question[-2]):
            #update score
            global score 
            score +=1
            # print(score)
            scoreLabel.config(text="Score: {}/{}".format(score, numQuestions))
            feedbackLabel.config(text="Correct!", foreground="green")
        else:
            feedbackLabel.config(text="Incorrect!", foreground="red")
            global wrongAnswers
            wrongAnswers += 1
    
    #if not int or float it is a multiple choice
    except:
        #check for multiple choice
        if selectedAnswer == question[-2]:
            #update score
            score +=1
            # print(score)
            scoreLabel.config(text="Score: {}/{}".format(score, numQuestions))
            feedbackLabel.config(text="Correct!", foreground="green")
            
        else:
            feedbackLabel.config(text="Incorrect!", foreground="red")
            wrongAnswers += 1

    #disable all answer buttons and enable the next button
    for button in answerBtns:
        button.config(state="disabled")
    submitButton.config(state="disabled")
    nextBtn.config(state="normal")

    continueOrNot()



#function to move to the next question
def nextQuestion():
    textBox.delete("1.0", "end-1c")
    global currentQuestion
    currentQuestion += 1
    currentQuestionLabel.config(text='Question '+str(currentQuestion+1))
    
    if currentQuestion < numQuestions:
        #if there are more questions show the next question
        showQuestion()
    else:
        #if all questions answered show finally score and say if pass or fail
        if (score / numQuestions) > .65:
            messagebox.showinfo("You Passed!", "Final Score: {}/{}".format(score, numQuestions))
        else:
            messagebox.showerror("You Failed.", "Final Score: {}/{}".format(score, numQuestions))
        root2.destroy()
        # createQuiz()

#adaptable part of test that determines if user can still pass
def continueOrNot():
    global msgBoxNotShown
    if wrongAnswers >= numToFail and msgBoxNotShown and currentQuestion+1 < numQuestions:
        msgBoxAnswer = messagebox.askquestion("You Failed.","You got too many questions wrong to be able to pass. Continue Anyway?")
        msgBoxNotShown = False
        if msgBoxAnswer == "no":
            root2.destroy()
    
    elif score >= numToPass and msgBoxNotShown and currentQuestion+1 < numQuestions:
        msgBoxAnswer = messagebox.askquestion("You Passed!","You got enough questions right to be able to pass. Continue Anyway?")
        msgBoxNotShown = False
        if msgBoxAnswer == "no":
            root2.destroy()


#creates the quiz window and its elements
def createQuiz():
    # print(quizArray)
    global root2
    root2 = tk.Tk()
    root2.geometry("1000x500")
    root2.title("Your Quiz!")

    #create current question label
    global currentQuestionLabel
    currentQuestionLabel = ttk.Label(root2, text='Question 1',padding=0)
    currentQuestionLabel.pack(pady=0)

    # Create question label
    global quesLabel
    quesLabel = ttk.Label(root2, text="hello",font=myFont)
    
    quesLabel.pack(pady=10)

    #Create the Answer Buttons
    global answerBtns
    answerBtns = []
    for i in range(4):
        button = ttk.Button(root2, command=lambda i=i: checkAnswer(i))
        button.pack(pady=10, ipadx=10,ipady=10)
        
        answerBtns.append(button)

    #create the fill in the blank textbox and hint
    global txtHintLbl
    txtHintLbl = ttk.Label(root2, text="Only use numbers, no words. Decimals can only be to the tenth place.")
    txtHintLbl.pack(pady=10)
    global textBox
    textBox = Text(root2,height=1,width=10)
    textBox.pack(pady=10)
    textBox.pack()

    #create textbox submit button
    global submitButton
    submitButton = ttk.Button(root2, text='Submit', command=lambda i="textbox":checkAnswer(i))
    submitButton.pack(pady=10, ipadx=10,ipady=10)

    #Create the right or wrong label
    global feedbackLabel
    feedbackLabel = ttk.Label(root2, anchor='center',)
    feedbackLabel.pack(pady=10)

    #Create the score label
    global scoreLabel
    scoreLabel = ttk.Label(
        root2,
        text="Score: 0/{}".format(numQuestions),
        anchor='center',
        padding=10)
    scoreLabel.pack()


    #Create the next Question button
    global nextBtn
    nextBtn = ttk.Button(root2, text='Next', command=nextQuestion, state="disabled", padding=10)
    nextBtn.configure()
    nextBtn.pack(pady=0)
    showQuestion()


#start main event loop
root.mainloop()  # Keep the window open