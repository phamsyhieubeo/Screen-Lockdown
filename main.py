import customtkinter as ctk
import subprocess
import tkinter as tk
from tkinter import messagebox
from time import sleep
import json
import os
import threading
from PIL import Image, ImageTk
import keyboard # type: ignore
import pygame
from discord_webhook import DiscordWebhook
import cv2

hook = DiscordWebhook(url= "https://discord.com/api/webhooks/1230312313714905170/TA_Yyt7diYjhurkSu7tMqV3k5gGOfyRyuTNVGFID3L031gRkH3LUgXWRq8K6jzfvCK_y")

def Leave_Message():
    with open("setting\\Setting.json", 'r') as f:
        data = json.load(f)
        Leave_Message_Value = data["Leaving_Message"]
        
    if Leave_Message_Value == 1:
        answer = messagebox.askquestion("Software", "Do you really want to leave? :<")
        if answer == "yes":
            messagebox.showinfo("Software", "See ya")
            sleep(0.2)
            quit()
        else:
            pass
    else:
        quit()
        
def Do_Nothing():
    pass
    

def disable_keyboard():
    keyboard.block_key("alt")
    keyboard.block_key("tab")
    keyboard.block_key("win")
    keyboard.block_key("ctrl")
    keyboard.block_key("esc")
    keyboard.block_key("f1")
    keyboard.block_key("f2")
    keyboard.block_key("f3")
    keyboard.block_key("f4")
    keyboard.block_key("f5")
    keyboard.block_key("f6")
    keyboard.block_key("f7")
    keyboard.block_key("f8")
    keyboard.block_key("f9")
    keyboard.block_key("f10")
    keyboard.block_key("f11")
    keyboard.block_key("f12")
    
def page_1():
    global Page_1
    
    Page_1 = ctk.CTkFrame(root, width= 450, height= 340)
    Page_1.pack()
    Page_1.propagate(0)
    Page_1.place(y = 25, x = 25)
        
    Title_Label = ctk.CTkLabel(Page_1, text= "Window's Lock down", font= ("Footlight MT Light", 50))
    Title_Label.pack()
    Title_Label.grid(sticky = "nsew")
    Title_Label.place(relx=0.5, rely=0.1, anchor='center')
    
    Start_Button = ctk.CTkButton(Page_1, text= "Lock down", font= ("Footlight MT Light", 16), width= 250, height= 40, command= Lockdown)
    Start_Button.pack()
    Start_Button.place(relx=0.5, rely=0.4, anchor='center')
    
    Setting_Button = ctk.CTkButton(Page_1, text= "Setting", font= ("Footlight MT Light", 16), width= 250, height= 40, command= lambda: SwitchPage(1, 2))
    Setting_Button.pack()
    Setting_Button.place(relx=0.5, rely=0.6, anchor='center')
    
    Quit_Button = ctk.CTkButton(Page_1, text= "Quit", font= ("Footlight MT Light", 16), width= 250, height= 40, command= Leave_Message)
    Quit_Button.pack()
    Quit_Button.place(relx=0.5, rely=0.8, anchor='center')

def setting_page():
    global Page_2, LeavingMessageSwitch_Variable
    
    # Load settings
    with open("setting\\Setting.json", 'r') as f:
        data = json.load(f)
    
    # State variables
    Appearance = tk.StringVar(value=data["Appearance"])
    Waiting_WallPaper = tk.StringVar(value=data["Waiting_Image"])
    LeavingMessageSwitch_Variable = ctk.IntVar(value=data["Leaving_Message"])
    
    # Setup page frame
    Page_2 = ctk.CTkFrame(root, width=450, height=340)
    Page_2.pack()
    Page_2.propagate(0)
    Page_2.place(y=25, x=25)
    
    # UI Components
    Title_Label = ctk.CTkLabel(Page_2, text="Settings", font=("Footlight MT Light", 50))
    Title_Label.pack()
    Title_Label.grid(sticky="nsew")
    Title_Label.place(relx=0.5, rely=0.1, anchor='center')
    
    Image_Box_Label = ctk.CTkLabel(Page_2, text= "Waiting Image", font=("Footlight MT Light", 16))
    Appearance_Label = ctk.CTkLabel(Page_2, text= "Appearance", font=("Footlight MT Light", 16))
    LeavingMessageSwitch_Label= ctk.CTkLabel(Page_2, text= "Leaving Message", font=("Footlight MT Light", 16))
    
    Image_Box_Label.place(relx= 0.1, rely=0.2)
    Appearance_Label.place(relx= 0.1, rely= 0.5)
    LeavingMessageSwitch_Label.place(relx = 0.6, rely = 0.2)
    
    Image_Box = ctk.CTkComboBox(Page_2, width=140, height=30, values=os.listdir("Res\\"), variable=Waiting_WallPaper)
    Image_Box.pack()
    Image_Box.place(relx = 0.1, rely=0.3)

    Appearance_ComboBox = ctk.CTkComboBox(Page_2, width=140, height=30, values=["Dark", "Light"], variable=Appearance)
    Appearance_ComboBox.pack()
    Appearance_ComboBox.place(relx=0.1, rely=0.6)

    LeavingMessageSwitch_Switch = ctk.CTkSwitch(Page_2, switch_width=50, switch_height=25, text="", variable=LeavingMessageSwitch_Variable)
    LeavingMessageSwitch_Switch.pack()
    LeavingMessageSwitch_Switch.place(relx=0.7, rely=0.3)
    
    def save_data():
        data["Waiting_Image"] = Image_Box.get()
        data["Appearance"] = Appearance.get()
        data["Leaving_Message"] = LeavingMessageSwitch_Variable.get()
        
        with open("setting\\Setting.json", 'w') as f:
            json.dump(data, f)
        ctk.set_appearance_mode(data["Appearance"])
        
    Apply_Button = ctk.CTkButton(Page_2, width=140, height=30, text="Apply", command=save_data)
    Apply_Button.pack()
    Apply_Button.place(relx=0.67, rely=0.9)

    Return_Button = ctk.CTkButton(Page_2, width=140, height=30, text="Return", command= lambda: SwitchPage(2, 1))
    Return_Button.pack()
    Return_Button.place(x = 12, rely=0.9)

LoginClicked = False
def StealerDetected():
    c = 0
    v = cv2.VideoCapture(0)
    while True:
        ret, frame = v.read()
        if c == 0:
            cv2.imwrite("Stealer.png", frame)
            c+= 1
        if c==1:
            break
    with open("Stealer.png", 'rb') as f:
        hook.add_file(f.read(), "Stealer.png")
    response = hook.execute()
    
stealer_thread = threading.Thread(target= StealerDetected)

def Login_Window(event):
    global LoginClicked
    if LoginClicked == False:
        LoginClicked = True
        loginWindow = ctk.CTk()
        loginWindow.geometry("330x250")
        loginWindow.resizable(0, 0)
        loginWindow.attributes('-topmost', True)
        
        def login_click():
            global LoginClicked
            LoginClicked = False
            loginWindow.destroy()
        loginWindow.protocol("WM_DELETE_WINDOW", login_click)
        loginWindow.attributes('-toolwindow', True)
        
        label = ctk.CTkLabel(loginWindow, text= "Login", font=("Footlight MT Light", 50))
        label.pack()
        
        username = ctk.CTkEntry(loginWindow, width= 240, height= 35, font=("Footlight MT Light", 26))
        username.pack()
        username.place(relx = 0.15, rely = 0.3)

        password = ctk.CTkEntry(loginWindow, width= 240, height= 35, font=("Footlight MT Light", 26), show = "*")
        password.pack()
        password.place(relx = 0.15, rely = 0.5)
        
        enter_button = ctk.CTkButton(loginWindow, width= 120, height= 35, font=("Footlight MT Light", 26), text = "Enter", command= lambda: check_account())
        enter_button.pack()
        enter_button.place(relx = 0.35, rely = 0.7)
        
        def check_account():
            with open("setting\\Account.json", 'r') as f:
                account_data = json.load(f)
            if username.get() in account_data["Username"]:
                if password.get() == account_data["Username"][username.get()]:
                    messagebox.showinfo("Software", "Welcome Back!")
                    loginWindow.destroy()
                    sleep(0.2)
                    root.destroy()
                else:
                    stealer_thread.start()    
                    messagebox.showerror("Software", "Error, Wrong Password or Username")
            else:
                messagebox.showerror("Software", "I cant find your account!")
                stealer_thread.start()
        loginWindow.mainloop()
        
block_key = threading.Thread(target= disable_keyboard)
def Lockdown():
    Page_1.destroy()
    root.attributes('-fullscreen', True)
    Img = Image.open(f"Res\\{data['Waiting_Image']}")
    Photo = ImageTk.PhotoImage(Img)
    ImgLabel = ctk.CTkLabel(root, image= Photo, text= "")
    ImgLabel.pack() 
    block_key.start()
    ImgLabel.bind("<Button-1>", Login_Window)
    
    
def PageChanger(page: int):
    if page == 1:
        page_1()
    if page == 2:
        setting_page()
    if page == 3:
        pass

def destroy_page(page: int):
    global Page_1
    global Page_2
    
    if page == 1:
        Page_1.destroy()
    if page == 2:
        Page_2.destroy()
    if page == 3:
        pass

def SwitchPage(CurrentPage: int, ToPage: int):
    global Page_1
    global Page_2
    if CurrentPage == 1:
        Page_1.destroy()
        PageChanger(ToPage)
    if CurrentPage == 2:
        Page_2.destroy()
        PageChanger(ToPage)

if __name__ == "__main__":
    root = ctk.CTk()
    root.geometry("500x400")
    root.resizable(0, 0)
    root.protocol("WM_DELETE_WINDOW", Leave_Message)
    root.bind_all("<Key>", Do_Nothing)
    
    with open("setting\\Setting.json", 'r') as f:
        data = json.load(f)
        Appearance = data["Appearance"]
        Waiting_WallPaper = data["Waiting_Image"]
    
    root.title(data["Title"])
    ctk.set_appearance_mode(Appearance)
    
    page_1()
    root.mainloop()
