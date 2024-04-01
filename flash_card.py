import random
from tkinter import *
from tkinter import messagebox
import pandas

GREEN = "#1E5128"
ORANGE = "#EB6440"
ORANGE_DARK = "#DC5F00"
answer = True
status = None

word_english = ""
word_spanish = ""

# --------------------------------------------- Buttons CLicked ---------------------------------------------- #
def check_button_clicked():
    global status,data_base
    if status == None:
        try :
            data_base = pandas.read_csv("data/words/words_to_learn.csv")
            data_base["english"]
            data_base["spanish"]
        except (FileNotFoundError, pandas.errors.EmptyDataError):
            try:
                data_base = pandas.read_csv("data/words/data_words.csv")
                data_base["english"]
                data_base["spanish"]
                data = pandas.DataFrame(data_base)
                data.to_csv("data/words/words_to_learn.csv",index=False)
            except:
                messagebox.showwarning("File not Found", "the archive data_words.csv not found")
                window.destroy()
        except:
            messagebox.showwarning("Wrong Data Base", "the archive words_to_learn.csv is corrupted")
            window.destroy()
        counting_down()
        return
    if answer:
        temp = data_base[data_base['english']!=word_english]
        data_base = temp
        messagebox.showinfo("Correct", "Correct Answer")
        data = pandas.DataFrame(data_base)
        data.to_csv("data/words/words_to_learn.csv",index=False)
    else:
        messagebox.showinfo("Wrong", "Wrong Answer")
    status = window.after(1000, counting_down)

def wrong_button_clicked():
    global status,data_base
    if status == None:
        window.destroy()
        return
    if not answer:
        temp = data_base[data_base['english']!=word_english]
        data_base = temp
        data = pandas.DataFrame(data_base)
        data.to_csv("data/words/words_to_learn.csv",index=False)
        messagebox.showinfo("Correct", "Correct Answer")
    else:
        messagebox.showinfo("Wrong", "Wrong Answer")
    status = window.after(1000, counting_down)  

# --------------------------------------------- Operations --------------------------------------------------- #
def change_language():
    global answer,data_base
    window.after_cancel(status)
    canvas.itemconfig(language_text,text="Español")
    if random.randint(0,1) == 1:
        answer = True
        canvas.itemconfig(word_text,text=word_spanish)
    else :
        answer = False
        temp = data_base[data_base['english']!=word_english]
        canvas.itemconfig(word_text,text = random.choice(temp['spanish']))
        
        

def counting_down():
    global status,data_base
    if len(data_base) == 0:
        messagebox.showinfo("Game Over", "You complete all words correctly")
        
        return
    global word_english,word_spanish
    word_english = random.choice(data_base['english']) 
    word_spanish = data_base[data_base['english']==word_english].iat[0,1]
    canvas.itemconfig(word_text,text=word_english,font=("Stencil",60,"bold"))
    canvas.itemconfig(language_text, text="English")
    status = window.after(3000, change_language)
    
# --------------------------------------------- UI SETUP ----------------------------------------------------- #
window = Tk()
window.title("Flashy")
icon = PhotoImage(file="data/images/icon.png")
window.iconphoto(True, icon)
window.config(padx=20,pady=20, bg=GREEN)



# Canvas Image
canvas = Canvas(width=600, height=350, bg=GREEN, highlightthickness=0)
card = PhotoImage(file="data/images/card.png")
card_canvas = canvas.create_image(300,200,image = card)
canvas.grid(column=0,row=0,columnspan=2)

# Canvas Text
language_text = canvas.create_text(300,80,text="Flash Card Game",font=("Stencil",30,"italic"),fill=ORANGE)
word_text = canvas.create_text(300,210,text=f"Press Check button\n            to start",font=("Stencil",40,"bold"),fill=ORANGE_DARK)


# Buttons
check_button_image = PhotoImage(file="data/images/check_button1.png")
check_button = Button(image=check_button_image,bg=GREEN, highlightthickness=0, command=check_button_clicked,pady=10,padx=10)
check_button.grid(column=0,row=1)

wrong_button_image = PhotoImage(file="data/images/wrong_button1.png")
wrong_button = Button(image=wrong_button_image,bg=GREEN,highlightthickness=0, command=wrong_button_clicked,pady=10,padx=10)
wrong_button.grid(column=1,row=1)

window.mainloop()

