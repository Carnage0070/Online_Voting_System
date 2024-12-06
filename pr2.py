from tkinter import *
from twilio.rest import Client
import random #for generating random no.s for OTP
import time
from tkinter import messagebox
from PIL import Image, ImageTk
import sys #to get command line args



class otp_verifier(Tk):
    def __init__(self,phone_number):
        super().__init__()
        self.geometry("1000x580+200+80")
        self.configure(bg = "cyan3")
        self.resizable(False, False)
        self.no_=str(self.OTP())
        self.client = Client("ACef3aa4c166a4733e1ab860d89cb8f949", "3e638f82d8d2b8bad81eb4067d08b016")
        self.client.messages.create(to=phone_number,
                      from_ ="+12317742092",
                     body = f"Your OTP is: {self.no_}")
    
        self.minuteString = StringVar()
        self.secondString = StringVar()
        

    ### Set strings to default value
        self.minuteString.set("00")
        self.secondString.set("30")
   
        
    def Labels(self):
        self.inner_box = Canvas(self,bg = "#808080", width=400 , height=280) # self=>in main otp window #Inner box/canva 
        self.inner_box.place(x = 290,y =120)
        #4682B4
        self.upper_frame = Frame(self , bg = "chocolate3" , width = 1500 , height = 130 )#creating the upper chocolate_color frame
        self.upper_frame.place(x=0,y=0)

        otp_image = Image.open("otp_pic.png").resize((100, 80), Image.LANCZOS)
        self.otp_picture = ImageTk.PhotoImage(otp_image)
        Label(self.upper_frame, image=self.otp_picture, bg="#4682B4").place(x=190, y=25)

        Label(self.upper_frame, text="Verify OTP", font = "TimesNewRoman 38 bold",bg= "#4682B4", fg="white").place(x= 300, y= 35) #Adding a text in the center of upper fram
        
        
        self.minuteTextbox = Entry(self, width=2,bg ="#808080", font=("Calibri", 20, ""), textvariable=self.minuteString)
        self.secondTextbox = Entry(self, width=2, bg ="#808080", font=("Calibri", 20, ""), textvariable=self.secondString)

### Center textboxes

        self.minuteTextbox.place(x=460, y=270)
        self.secondTextbox.place(x=500, y=270)
        
           
    def Entry(self): #we will enter the otp here
        self.User_Name = Text(self, font="calibri 20", borderwidth = 2,wrap = WORD, width = 23 , height = 1 ) #"Text" Widget is used to input the multiline texts, we can also add images in it. 
                                                                                                              #Borderwidth=>so as to see in the canvas. Wrap=>if word limit exceeds, then goes to the next line
        self.User_Name.place(x = 330,y = 200)
    
    def OTP(self):
        return random.randrange(1000,10000)

    def Buttons(self):
        submit_image = Image.open("submit_pic.png").resize((150, 50), Image.LANCZOS)
        self.submitButtonImage = ImageTk.PhotoImage(submit_image)
        self.submitButton = Button(self, image=self.submitButtonImage, command=lambda: [self.checkOTP(), self.runTimer()], border=0)
        self.submitButton.place(x=400, y=330)
        
        resend_image = Image.open("resendotp_pic.png").resize((150, 50), Image.LANCZOS)
        self.resendOTPImage = ImageTk.PhotoImage(resend_image)
        self.resendOTP = Button(self, image=self.resendOTPImage, command=self.resendOTP, border=0)
        self.resendOTP.place(x=400, y=400)
        
    def resendOTP(self):
        self.no_ = str(self.OTP())
        self.client = Client("ACef3aa4c166a4733e1ab860d89cb8f949", "3e638f82d8d2b8bad81eb4067d08b016")
        self.client.messages.create(
            to=sys.argv[1],  # Send OTP to the same phone number passed earlier
            from_="+12317742092",
            body=f"Your new OTP is: {self.no_}"
        )
       
    
    def checkOTP(self):
        try:
            self.userInput=int(self.User_Name.get(1.0, "end-1c"))#takes the string passed nd converts into int, wr the value is taken frm User_Name  
            if self.userInput == int(self.no_): #if the entered otp is correct then:
                messagebox.showinfo ("showinfo", "Verification Successful") #displaying this message
                self.no_ = "done" #serves as a flag to indicate that the OTP verification has been completed successfully, which avoids Re-verification/prevents OTP reuse
            else:
                messagebox.showinfo("showinfo", "wrong OTP")
        except:
            messagebox.showinfo ("showinfo", "INVALID OTP ") 
    
    def runTimer(self):
        
        self.clockTime = int(self.minuteString.get())*60 + int(self.secondString.get())
        self.countdown()

    def countdown(self):
        if self.clockTime <= 0:
            messagebox.showinfo("Time out", "Your time has expired!")
            return
        
        # Calculate minutes and seconds
        totalMinutes, totalSeconds = divmod(self.clockTime, 60)
        self.minuteString.set(f"{totalMinutes:02d}")
        self.secondString.set(f"{totalSeconds:02d}")

    # Update time and schedule next call
        self.clockTime -= 1
        self.after(1000, self.countdown)  # Schedule countdown to run again in 1 second

        
            
if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise ValueError("Phone number not provided!")
    phone_number = sys.argv[1]  # Get phone number passed as argument
    window = otp_verifier(phone_number)
    window.Labels()
    window.Entry()
    window.OTP()
    window.Buttons()
    window.update()
    window.mainloop()