import mysql.connector as c
from tkinter import *
import customtkinter as ctk 
from datetime import * 
import random as rand
from PIL import ImageTk, Image
import time
import subprocess
from twilio.rest import Client
import threading



con = c.connect(host='localhost',user='root',passwd='galphoe3000',database='nix')
cursor = con.cursor()

mainUi_status = False

global currentuser
currentuser = []

gif_frames = []

frames_delay = 0
                    # for payment animation gif
stop = False

frame_count = -1 

transaction_details = []
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Backend Functions~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def stayLoggedIn():
    try :
        global uuid
        uuid = subprocess.check_output('wmic bios get serialnumber').decode("utf-8") 
        li = list(uuid.split(" "))
        li[5] = li[5].replace("\r",'')
        li[5] = li[5].replace("\n",'')
        uuid = li[5]


        cursor.execute(f"SELECT STATUS FROM LOGIN_STATUS WHERE UUID = '{uuid}';")
        uuid_check = cursor.fetchone()
        
        if uuid_check == None :
            cursor.execute(f"INSERT INTO LOGIN_STATUS VALUES('{uuid}',NULL,NULL);")
            con.commit()
        else: 
            pass
        
        cursor.execute(f"SELECT STATUS FROM LOGIN_STATUS WHERE UUID = '{uuid}';")
        status = cursor.fetchone()

        if status[0] == None :
            login_win()
        elif status[0] == "True" :
            cursor.execute(f"SELECT PHNO FROM LOGIN_STATUS WHERE UUID = '{uuid}';")
            al_phno = cursor.fetchone()
            currentuser.append(int(al_phno[0]))
            mainUI()
        
    except Exception as e:
        print(e)

def mainFunction():
    global phonenumber
    phonenumber = phno.get()
    password = passwd.get()

    try :
        phonenumber = int(phonenumber)
        phno.configure(text_color = "#494949",border_width = 0,font=("Barlow",25,'normal'))
    
        cursor.execute(f"SELECT PHONE_NO,PASSWORD FROM USER_DETAILS WHERE PHONE_NO={phonenumber};")
        feedback = cursor.fetchone()
        
        if feedback == None :
            validstStr.set("User does not exist")
            passwd.configure(border_width=3,border_color="#C21807")
            phno.configure(border_width=3,border_color="#C21807")
        elif feedback != None and feedback[1] != password :
            validstStr.set("Incorrect Password")
            passwd.configure(border_width=3,border_color="#C21807")
        elif feedback != None and feedback[1] == password :
            validstStr.set("")
            passwd.configure(border_width=0)
            phno.configure(border_width=0)
            otp_win()
            


    except Exception as fuc_:
        phnoStr = ctk.StringVar()
        print(fuc_)
        phnoStr.set('Enter valid phone no')
        phno.configure(text_color = "#C21807",border_width = 3,border_color="#C21807",textvariable=phnoStr,font=("Barlow",13,'normal'))

def get_otp(cpno):
  global genotp
  genotp = rand.randrange(111111,999999)
  try:
    account_sid = '<Account ID>'
    auth_token = '<Auth Token>'
    client = Client(account_sid, auth_token)

    
    
    
    
    
    message = client.messages.create(
        from_='+13203318192',
        body='OTP from NIX : {otp}'.format(otp = genotp),
        to=f'+91{cpno}')
    print(genotp)
  except:
    print(genotp)
  
def timerfn():
  timer.configure(text="01:00")
  resendtime = 60
  while resendtime > 0 :
    resendtime -= 1
    timer.configure(text="00:{t}".format(t=resendtime))
    otpwin.update()
    time.sleep(1)
    if resendtime > 0 :
      timer.configure(text="00:59")
  
    if resendtime == 0:
      timer.configure(text="00:00")
      resend.configure(state=NORMAL)
    
    if resendtime < 10:
      timer.configure(text="00:0{t}".format(t=resendtime))

def otpverification():
  otp = otpentry.get()
  try :
    otp = int(otp)
    if otp == genotp:
      otpstatus.configure(text_color="#494949")
      otpentry.configure(text_color = "#494949",border_width = 0,font=("Barlow",13,'normal'))
      try:
        timer.destroy()
        otpwin.destroy()
        login.destroy()



        cursor.execute(f"UPDATE LOGIN_STATUS SET STATUS = 'True' WHERE UUID = '{uuid}';")
        con.commit()
        cursor.execute(f"UPDATE LOGIN_STATUS SET PHNO = {phonenumber} WHERE UUID = '{uuid}';")
        con.commit()


        currentuser.append(phonenumber)

        if mainUi_status == False :
          mainUI()
          mainUi_status = True
      except Exception as bruh:
         pass
        #  print(bruh)

    else :
      otpentry.configure(text_color = "#C21807",border_width = 1,border_color="#926EEF",font=("Barlow",13,'normal'))
      otpstatus.configure(text_color="red",text="Invalid OTP")

  except Exception as fuc_:
      print(fuc_)
      otpstatus.configure(text_color="red",text="Enter Valid OTP")
      otpentry.configure(text_color = "#C21807",border_width = 3,border_color="#C21807",font=("Barlow",13,'normal'))

def resendfn():
   get_otp()
   timerfn()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Frontend Functions~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def splashScreen():
    w = Tk()
    width_of_window = 427
    height_of_window = 250
    global screen_width
    screen_width = w.winfo_screenwidth()
    global screen_height
    screen_height = w.winfo_screenheight()
    x_coord = (screen_width/2)-(width_of_window/2)
    y_coord = (screen_height/2)-((height_of_window/2)+25)
    w.geometry("%dx%d+%d+%d" %(width_of_window,height_of_window,x_coord,y_coord))
    w.overrideredirect(1)     #for hiding titlebar


    Frame(w,width=427,height=250,bg='#272727').place(x=0,y=0)


    #animation

    image_a = ImageTk.PhotoImage(Image.open('Splash_Screen/Untitled.png'))
    image_b = ImageTk.PhotoImage(Image.open('Splash_Screen/Untitled3.png'))
    image_c = ImageTk.PhotoImage(Image.open('Splash_Screen/nix_splash.png'))
    image_d = ImageTk.PhotoImage(Image.open('Splash_Screen/Untitled2.png'))
    label3 = Label(w,image=image_c,border=0,relief=SUNKEN,bg = '#272727').place(x=-60,y=0)

    label2 = Label(w,text='Loading...',fg = 'white',bg = '#1E1E1E')
    label2.configure(font=("Calibri", 11))
    label2.place(x=5,y=220)

    for i in range(5):
        l1 = Label(w,image=image_a,border=0,relief=SUNKEN).place(x=180,y=170)
        l2 = Label(w,image=image_b,border=0,relief=SUNKEN).place(x=200,y=170)
        l3 = Label(w,image=image_b,border=0,relief=SUNKEN).place(x=220,y=170)
        l4 = Label(w,image=image_b,border=0,relief=SUNKEN).place(x=240,y=170)
        w.update_idletasks()
        time.sleep(0.5)

        l1 = Label(w,image=image_b,border=0,relief=SUNKEN).place(x=180,y=170)
        l2 = Label(w,image=image_d,border=0,relief=SUNKEN).place(x=200,y=170)
        l3 = Label(w,image=image_b,border=0,relief=SUNKEN).place(x=220,y=170)
        l4 = Label(w,image=image_b,border=0,relief=SUNKEN).place(x=240,y=170)
        w.update_idletasks()
        time.sleep(0.5)

        l1 = Label(w,image=image_b,border=0,relief=SUNKEN).place(x=180,y=170)
        l2 = Label(w,image=image_b,border=0,relief=SUNKEN).place(x=200,y=170)
        l3 = Label(w,image=image_a,border=0,relief=SUNKEN).place(x=220,y=170)
        l4 = Label(w,image=image_b,border=0,relief=SUNKEN).place(x=240,y=170)
        w.update_idletasks()
        time.sleep(0.5)

        l1 = Label(w,image=image_b,border=0,relief=SUNKEN).place(x=180,y=170)
        l2 = Label(w,image=image_b,border=0,relief=SUNKEN).place(x=200,y=170)
        l3 = Label(w,image=image_b,border=0,relief=SUNKEN).place(x=220,y=170)
        l4 = Label(w,image=image_d,border=0,relief=SUNKEN).place(x=240,y=170)
        w.update_idletasks()
        time.sleep(0.5)

        if i == 2 :
            label2.configure(text="Collecting...")

    w.destroy()
    stayLoggedIn()


    w.mainloop()

def login_win():
    global login
    login = ctk.CTk()
    login.title("Nix")
    login.wm_iconbitmap("NixIcon.ico")
    width_of_login = 1080
    height_of_login = 600
    # global screen_width
    screen_width = login.winfo_screenwidth()
    # global screen_height
    screen_height = login.winfo_screenheight()
    x_coordl = ((screen_width/2)+50)-(width_of_login/2)
    y_coordl = ((screen_height/2))-((height_of_login/2)+25)
    login.geometry("%dx%d+%d+%d" %(width_of_login,height_of_login,x_coordl,y_coordl))
    login.resizable(False,False)

    login.grid_columnconfigure(0,weight=2)
    login.grid_columnconfigure(1,weight=3)
    login.grid_rowconfigure((0,1),weight= 1)

    frame = ctk.CTkFrame(login,corner_radius=10,fg_color='#121212',width= 1070,height=590)
    frame.pack(pady=5)

    global t
    t=['False']

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~GUI~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    vector = Image.open('LoginWindow/Vectors.png')
    vector = vector.resize((550,670))
    vector.save('LoginWindow/Vectors.png')
    vector = ImageTk.PhotoImage(Image.open('LoginWindow/Vectors.png'))
    l1 = Label(login,image=vector,border=0,bg="#121212" ,relief=SUNKEN).place(x=10,y=35)

    nixlogo = Image.open('LoginWindow/NixIcon.png')
    nixlogo = nixlogo.resize((55,55))
    nixlogo.save('LoginWindow/NixIcon.png')
    nixlogo = ImageTk.PhotoImage(Image.open('LoginWindow/NixIcon.png'))
    l2 = Label(login,image=nixlogo,border=0,bg="#121212" ,relief=SUNKEN).place(x=13,y=8)

    nixlogo2 = Image.open('LoginWindow/Nix Logo 2.png')
    nixlogo2 = nixlogo2.resize((75,53))
    nixlogo2.save('LoginWindow/Nix Logo 2.png')
    nixlogo2 = ImageTk.PhotoImage(Image.open('LoginWindow/Nix Logo 2.png'))
    l3 = Label(login,image=nixlogo2,border=0,bg="#121212" ,relief=SUNKEN).place(x=1257,y=8)

    wlcmheader = Image.open('LoginWindow/Welcomeheader.png')
    wlcmheader = wlcmheader.resize((610,142))
    wlcmheader.save('LoginWindow/Welcomeheader.png')
    wlcmheader = ImageTk.PhotoImage(Image.open('LoginWindow/Welcomeheader.png'))
    l4 = Label(login,image=wlcmheader,border=0,bg="#121212" ,relief=SUNKEN).place(x=700,y=80)

    txtflds = Image.open('LoginWindow/TextFields.png')
    txtflds = txtflds.resize((590,263))
    txtflds.save('LoginWindow/TextFields.png')
    txtflds = ImageTk.PhotoImage(Image.open('LoginWindow/TextFields.png'))
    l4 = Label(login,image=txtflds,border=0,bg="#121212" ,relief=SUNKEN).place(x=700,y=290)

    global phno
    phno = ctk.CTkEntry(login,height=56,width=465
                            ,fg_color='#292929'
                            ,bg_color='transparent'
                            ,text_color='#494949'
                            ,placeholder_text='Phone No'
                            ,placeholder_text_color='#494949'
                            ,font=("Barlow",25)
                            ,corner_radius=11
                            ,border_width=0
                            )
    phno.place(x=563,y=244)

    global labelPhno
    labelPhno = ctk.CTkLabel(login,text="Phone No",font=("Barlow",10,'normal'),text_color='#121212',fg_color='#121212',bg_color='#121212')
    labelPhno.place(x=568,y=204) 

    phno.bind('<KeyPress>',appearph)





    global passwd
    passwd = ctk.CTkEntry(login,height=56,width=465
                            ,fg_color='#292929'
                            ,bg_color='transparent'
                            ,text_color='#494949'
                            ,show='*'
                            ,placeholder_text='Password'
                            ,placeholder_text_color='#494949'
                            ,font=("Barlow",25)
                            ,corner_radius=11
                            ,border_width=0
                            )
    passwd.place(x=563,y=382)


    global labelpass
    labelpass = ctk.CTkLabel(login,text="Password",font=("Barlow",10,'normal'),text_color='#121212',fg_color='#121212',bg_color='#121212')
    labelpass.place(x=568,y=343) 

    passwd.bind('<KeyPress>',appearps)


    global hide_pass
    hide_pass = ctk.CTkImage(Image.open('LoginWindow/closed_eye.png'),size = (28,11))
    global show_pass
    show_pass = ctk.CTkImage(Image.open('LoginWindow/open_eye.png'),size = (30,30))
    global l13
    l13 = ctk.CTkLabel(login,text='',image=hide_pass,bg_color="#292929")
    l13.place(x=990,y=400)
    l13.bind('<Button>',set_pass_mode)





    mask1 = Image.open('Login_Txt_Borders\Mask group1.png')
    mask1 = mask1.resize((10,12))
    mask1.save('Login_Txt_Borders\Mask group1.png')
    mask1 = ImageTk.PhotoImage(Image.open('Login_Txt_Borders\Mask group1.png'))
    l5 = Label(login,image=mask1,border=0,bg="#121212" ,relief=SUNKEN).place(x=699,y=542)

    mask2 = Image.open('Login_Txt_Borders\Mask group2.png')
    mask2 = mask2.resize((12,12))
    mask2.save('Login_Txt_Borders\Mask group2.png')
    mask2 = ImageTk.PhotoImage(Image.open('Login_Txt_Borders\Mask group2.png'))
    l6 = Label(login,image=mask2,border=0,bg="#121212" ,relief=SUNKEN).place(x=700,y=473)

    mask3 = Image.open('Login_Txt_Borders\Mask group3.png')
    mask3 = mask3.resize((10,12))
    mask3.save('Login_Txt_Borders\Mask group3.png')
    mask3 = ImageTk.PhotoImage(Image.open('Login_Txt_Borders\Mask group3.png'))
    l7 = Label(login,image=mask3,border=0,bg="#121212" ,relief=SUNKEN).place(x=1280,y=471)

    mask4 = Image.open('Login_Txt_Borders\Mask group4.png')
    mask4 = mask4.resize((10,12))
    mask4.save('Login_Txt_Borders\Mask group4.png')
    mask4 = ImageTk.PhotoImage(Image.open('Login_Txt_Borders\Mask group4.png'))
    l8 = Label(login,image=mask4,border=0,bg="#121212" ,relief=SUNKEN).place(x=1280,y=538)

    mask5 = Image.open('Login_Txt_Borders\Mask group5.png')
    mask5 = mask5.resize((13,13))
    mask5.save('Login_Txt_Borders\Mask group5.png')
    mask5 = ImageTk.PhotoImage(Image.open('Login_Txt_Borders\Mask group5.png'))
    l9 = Label(login,image=mask5,border=0,bg="#121212" ,relief=SUNKEN).place(x=696,y=297)

    mask6 = Image.open('Login_Txt_Borders\Mask group6.png')
    mask6 = mask6.resize((12,12))
    mask6.save('Login_Txt_Borders\Mask group6.png')
    mask6 = ImageTk.PhotoImage(Image.open('Login_Txt_Borders\Mask group6.png'))
    l10 = Label(login,image=mask6,border=0,bg="#121212" ,relief=SUNKEN).place(x=698,y=368)

    mask7 = Image.open('Login_Txt_Borders\Mask group7.png')
    mask7 = mask7.resize((12,12))
    mask7.save('Login_Txt_Borders\Mask group7.png')
    mask7 = ImageTk.PhotoImage(Image.open('Login_Txt_Borders\Mask group7.png'))
    l11 = Label(login,image=mask7,border=0,bg="#121212" ,relief=SUNKEN).place(x=1281,y=297)

    mask8 = Image.open('Login_Txt_Borders\Mask group8.png')
    mask8 = mask8.resize((9,9))
    mask8.save('Login_Txt_Borders\Mask group8.png')
    mask8 = ImageTk.PhotoImage(Image.open('Login_Txt_Borders\Mask group8.png'))
    l12 = Label(login,image=mask8,border=0,bg="#121212" ,relief=SUNKEN).place(x=1277,y=370)


    loginbtn = ctk.CTkButton(login
                             ,width=475
                             ,height=52
                             ,corner_radius=33
                             ,border_width=0
                             ,text="L O G I N"
                             ,text_color='white'
                             ,font=('Barlow Medium',20,'normal')
                             ,hover=True
                             ,fg_color='#9436CC'
                             ,hover_color= '#6437DF'
                             ,bg_color='#121212'
                             ,command=mainFunction)
    loginbtn.place(x=560,y=500)


    global fgpass
    fgpass = ctk.CTkLabel(login,text="Forgot Password",font=('Barlow',17,'normal'),text_color='#494949',fg_color='#121212',bg_color='#121212')
    fgpass.place(x=880,y=455)

    fgpass.bind('<Enter>',hover_infg)
    fgpass.bind('<Leave>',hover_outfg)


    newhere = ctk.CTkLabel(login,text="New Here?",font=('Barlow',17,'normal'),text_color='#494949',fg_color='#121212',bg_color='#121212')
    newhere.place(x=580,y=455)

    global register
    register = ctk.CTkLabel(login,text="  Register",font=('Barlow',17,'normal'),text_color='#B31099',fg_color='#121212',bg_color='#121212')
    register.place(x=660,y=455)

    register.bind('<Enter>',hover_inrg)
    register.bind('<Leave>',hover_outrg)

    global validstStr
    validstStr = ctk.StringVar()
    valid_status = ctk.CTkLabel(login,font=("Barlow",17,'normal'),text_color='red',fg_color='#121212',bg_color='#121212',textvariable=validstStr)
    valid_status.place(x=885,y=310)



    login.mainloop()

def otp_win():
    try :
      global otpwin
      otpwin = ctk.CTkToplevel()
      otpwin.title("Nix")
      otpwin.wm_iconbitmap("NixIcon.ico")
      width_of_otpwin = 350
      height_of_otpwin = 350
      screen_width = otpwin.winfo_screenwidth()
      screen_height = otpwin.winfo_screenheight()
      x_coordl = ((screen_width/2)+90)-(width_of_otpwin/2)
      y_coordl = ((screen_height/2))-((height_of_otpwin/2)-40)
      otpwin.geometry("%dx%d+%d+%d" %(width_of_otpwin,height_of_otpwin,x_coordl,y_coordl))
      otpwin.resizable(False,False)

      otpframe = ctk.CTkFrame(otpwin,corner_radius=10,fg_color='#121212',width= 340,height=340)
      otpframe.pack(pady=5)

      

      nixlogo_otp = ImageTk.PhotoImage(Image.open('LoginWindow/NixIcon.png'))
      l2 = Label(otpframe,image=nixlogo_otp,border=0,bg="#121212" ,relief=SUNKEN)
      l2.place(x=360,y=8)
      
      nixlogo2_otp = ImageTk.PhotoImage(Image.open('LoginWindow/Nix Logo 2.png'))
      l3 = Label(otpframe,image=nixlogo2_otp,border=0,bg="#121212" ,relief=SUNKEN)
      l3.place(x=25,y=8)

      l1 =  ctk.CTkLabel(otpframe,text='An OTP was sent to {ph}'.format(ph=phonenumber)
                        ,text_color="#494949"
                        ,bg_color="#121212"
                        ,fg_color="#121212"
                        ,font=('Barlow',14,'normal'))
      l1.place(x=20,y=60)

      global otpentry
      otpentry = ctk.CTkEntry(otpframe,width=300,height=41
                            ,text_color="#494949"
                            ,placeholder_text="Enter OTP"
                            ,placeholder_text_color="#494949"
                            ,border_width=1
                            ,border_color="#926EEF"
                            ,font=('Barlow',14,'normal')
                            ,fg_color="#121212")
      otpentry.place(x=18,y=90)


      otpbutton = ctk.CTkButton(otpframe
                             ,width=300
                             ,height=30
                             ,corner_radius=33
                             ,border_width=0
                             ,text="L O G I N"
                             ,text_color='white'
                             ,font=('Barlow Medium',20,'normal')
                             ,hover=True
                             ,fg_color='#9436CC'
                             ,hover_color= '#6437DF'
                             ,bg_color='#121212'
                             ,command=otpverification)
      otpbutton.place(x=18,y=220)

      global resend
      resend = ctk.CTkButton(otpframe
                             ,width=100
                             ,height=30
                             ,corner_radius=33
                             ,border_width=0
                             ,text="RESEND"
                             ,text_color='white'
                             ,font=('Barlow',13,'normal')
                             ,hover=True
                             ,fg_color='#9436CC'
                             ,hover_color= '#6437DF'
                             ,bg_color='#121212'
                             ,state=DISABLED
                             ,command=resendfn)
      resend.place(x=118,y=270)


      global timer
      timer = ctk.CTkLabel(otpframe,text="09:11",text_color="#926EEF",font=('Barlow ExtraBold',40,'normal'),fg_color='#121212',bg_color='#121212')
      timer.place(x=125,y=143)

      global otpstatus
      otpstatus = ctk.CTkLabel(otpframe,text="Invalid OTP",font=("Barlow Medium",12,'normal'),text_color='#121212',fg_color='#121212',bg_color='#121212')
      otpstatus.place(x=250,y=130)







      get_otp(phonenumber)
      timerfn()
      otpwin.mainloop()
    
    except Exception as why:
       #print(why)
       cursor.execute(f"UPDATE LOGIN_STATUS SET STATUS = 'True' WHERE UUID = '{uuid}';")
       con.commit()
       mainUI()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~UI Fucntions~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def hover_infg(e):
    fgpass.configure(text_color='#654EEC')

def hover_outfg(e):
    fgpass.configure(text_color='#494949')

def hover_inrg(e):
    register.configure(text_color='#6437DF')

def hover_outrg(e):
    register.configure(text_color='#B31099')

def appearph(e):
    labelPhno.configure(text_color='#494949',font=('Barlow',17,'normal'))

def appearps(e):
    labelpass.configure(text_color='#494949',font=('Barlow',17,'normal'))

def set_pass_mode(e):
   if t[0] == 'False' :
    t[0] = 'True'
    show_hide_pass()

   elif t[0] == 'True' :
    t[0] = 'False'
    show_hide_pass()

def show_hide_pass():
   if t[0] == 'True' :
      
      l13.configure(image= show_pass)
      passwd.configure(show='')
      l13.place(x=990,y=395)
      login.update()
      

   elif t[0] == 'False' :
      
      l13.configure(image= hide_pass)
      passwd.configure(show='*')
      l13.place(x=990,y=400)
      login.update()

def mainUI():
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~BACKEND~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def ecard_details():
    
        cursor.execute(f'SELECT ACCOUNT_DETAILS.BALANCE,ACCOUNT_DETAILS.CARD_NO,ACCOUNT_DETAILS.EXP_DATE FROM USER_DETAILS,ACCOUNT_DETAILS WHERE USER_DETAILS.ACCOUNT_NO = ACCOUNT_DETAILS.ACCOUNT_NO AND USER_DETAILS.PHONE_NO = {currentuser[0]};')
        carddetails = cursor.fetchone()
        
        global cardno
        cardno = ''
        icardno = str(carddetails[1])
        for n in range(len(icardno)):
            if n == 4 or n == 8 :
                cardno+='   '
                cardno+=icardno[n]
            elif n in [0,1,2,3,4,5,6,7,8,9,10,11]:
                cardno+=' '
                cardno+=icardno[n]
            else:
                cardno+=icardno[n]
                
        global expdate 
        expdate = carddetails[2]
        global balance
        balance = carddetails[0]

        global censored_cardno
        censored_cardno = f"● ● ● ●   {cardno[21:]}"
    
    def payment_gateway():
        if transfer_to_entry.get() != 'Phone Number' and amount.get() != 'Amount, Rupees':
            try:
                verify_transfer_no = transfer_to_entry.get()
                verify_amount = amount.get()
                try:
                    verify_transfer_no = int(verify_transfer_no)
                    try:
                        verify_amount = int(verify_amount)
                        if verify_transfer_no == currentuser[0]:
                            validation_var.set('Can\'t send money to self')    
                        else:
                            cursor.execute(f'SELECT ACCOUNT_DETAILS.BALANCE FROM USER_DETAILS,ACCOUNT_DETAILS WHERE USER_DETAILS.ACCOUNT_NO = ACCOUNT_DETAILS.ACCOUNT_NO AND USER_DETAILS.PHONE_NO = {currentuser[0]};')
                            amt_presence_feedback = cursor.fetchone()

                            cursor.execute(f'SELECT ACCOUNT_DETAILS.BALANCE FROM USER_DETAILS,ACCOUNT_DETAILS WHERE USER_DETAILS.ACCOUNT_NO = ACCOUNT_DETAILS.ACCOUNT_NO AND USER_DETAILS.PHONE_NO = {verify_transfer_no};')
                            presence_feedback = cursor.fetchone()

                            if presence_feedback == None:
                                validation_var.set('User doesnt exist')
                                amount.configure(text_color = "white",border_color="#2e2e2e",font=("Barlow",13,'normal'))
                                transfer_to_entry.configure(text_color = "white",border_color="#2e2e2e",font=("Barlow",13,'normal'))
                            elif presence_feedback[0] != None:
                                if verify_amount > amt_presence_feedback[0] :
                                    validation_var.set('Insuffucient Balance')
                                else:
                                    if len(payment_type) > 0:
                                        validation_var.set('')
                                        transaction_details.append(verify_transfer_no)
                                        transaction_details.append(verify_amount)
                                        transaction_details.append(payment_type[0])
                                        transaction_details.append(presence_feedback[0])
                                        upi_transaction_page()
                                        
                                    else:
                                        validation_var.set('Please choose spending type')        
                    
                    except Exception as p:
                        rec_amtStr.set('Enter valid amount')
                        
                        transfer_to_entry.configure(text_color = "white",border_color="#2e2e2e",font=("Barlow",13,'normal'))
                        amount.configure(text_color = "#C21807",border_color="#C21807",textvariable=rec_amtStr,font=("Barlow",13,'normal'))


                except:
                    rec_phnoStr.set('Enter valid phone no')
                    if rec_amtStr.get() != 'Amount, Rupees':
                        amount.configure(text_color = "white",border_color="#2e2e2e",font=("Barlow",13,'normal'))
                    transfer_to_entry.configure(text_color = "#C21807",border_color="#C21807",textvariable=rec_phnoStr,font=("Barlow",13,'normal'))
                    

                
                
            except Exception as kyadikkathorhi :
                print(kyadikkathorhi) 
        else:
            pass

    def upi_pin_verification():
        try :

            if upipin_entry1.get() != "" and upipin_entry2.get() != ""  and upipin_entry3.get() != ""  and upipin_entry4.get() != "" :
                upi_digits = [upipin_entry1.get(),upipin_entry2.get(),upipin_entry3.get(),upipin_entry4.get()]
                upi_pin = ''


                for upi_get in upi_digits:
                    upi_pin+=upi_get
                
                try:
                    upi_pin = int(upi_pin)
                    cursor.execute(f"SELECT UPI_PIN FROM ACCOUNT_DETAILS WHERE ACCOUNT_NO = {currentuser[1]};")
                    valid_upi_check = cursor.fetchone()

                    if valid_upi_check[0] == upi_pin:
                        payment_transaction(transaction_details[0],transaction_details[1],transaction_details[2],transaction_details[3])
                        
                    else:
                        upi_valid_var.set('Invalid UPI pin')
                        upipin_entry1.delete(0)
                        upipin_entry2.delete(0)
                        upipin_entry3.delete(0)
                        upipin_entry4.delete(0)
                        upipin_entry1.focus()

                except:
                    upi_valid_var.set('Enter valid UPI pin')
                    
                    upipin_entry1.delete(0)
                    upipin_entry1.configure(border_color='red')
                    upipin_entry2.delete(0)
                    upipin_entry2.configure(border_color='red')
                    upipin_entry3.delete(0)
                    upipin_entry3.configure(border_color='red')
                    upipin_entry4.delete(0)
                    upipin_entry4.configure(border_color='red')
                    upipin_entry1.focus()

            
            
            else:
                pass


        except:
            pass

    def payment_transaction(rphno,ramt,stype,rbalance):
        time.sleep(3)
        try :
            t_datetime = datetime.now()
            t_date = datetime.strptime(t_datetime.strftime("%d/%m/%Y %H:%M:%S"),"%d/%m/%Y %H:%M:%S")
            

            cursor.execute(f'SELECT ACCOUNT_DETAILS.CARD_NO,ACCOUNT_DETAILS.ACCOUNT_NO,ACCOUNT_DETAILS.BALANCE FROM USER_DETAILS,ACCOUNT_DETAILS WHERE USER_DETAILS.ACCOUNT_NO = ACCOUNT_DETAILS.ACCOUNT_NO AND USER_DETAILS.PHONE_NO = {currentuser[0]};')
            sdetails = cursor.fetchone()
            scardno = sdetails[0]
            saccno = sdetails[1]
            sbalance = sdetails[2]

            cursor.execute(f'SELECT USERNAME,ACCOUNT_NO FROM USER_DETAILS WHERE PHONE_NO = {rphno};')
            rdetails = cursor.fetchone()
            rname = rdetails[0]
            raccno = rdetails[1]
            
            cursor.execute(f"INSERT INTO TRANSACTIONS VALUES({saccno},{scardno},'{rname}',{raccno},'{stype}','{t_date}',{ramt},'{currentuser[2]}');")
            con.commit()
            


            cursor.execute(f"UPDATE ACCOUNT_DETAILS SET BALANCE = {sbalance-ramt} WHERE ACCOUNT_NO = {saccno};")
            con.commit()
            
            cursor.execute(f"UPDATE ACCOUNT_DETAILS SET BALANCE = {rbalance+ramt} WHERE ACCOUNT_NO = {raccno};")
            con.commit()

            trnsctn_success(ramt,rphno)


        except Exception as error :
            print(error)

    def create_history(item,p): 
        

        if p == 'hp':
            history_overframe = ctk.CTkFrame(historydetailframe,fg_color='#161616')
        
            img = ctk.CTkImage(Image.open('icons/profilepic.png'),size=(30,30))
            if item[0] == currentuser[1] :
                ctk.CTkButton(history_overframe,height=90,image=img,
                                        fg_color='#161616',bg_color='#161616',
                                        text=f"                       To {item[2]}                                                                                                                                          {item[5]}                                                                                           -₹ {item[6]}",
                                        text_color='#2e2e2e',font=("Barlow SemiBold",20),
                                        border_width=3,border_color='#2e2e2e',
                                        hover=False,corner_radius=10,compound=LEFT,anchor='w').pack(fill='x')
            else:
                ctk.CTkButton(history_overframe,height=90,image=img,
                                        fg_color='#161616',bg_color='#161616',
                                        text=f"                        From {item[7]}                                                                                                                                  {item[5]}                                                                                           +₹ {item[6]}",
                                        text_color='#2e2e2e',font=("Barlow SemiBold",20),
                                        border_width=3,border_color='#2e2e2e',
                                        hover=False,corner_radius=10,compound=LEFT,anchor='w').pack(fill='x')
            return history_overframe
        
        elif p == 'rs':
            pass

        elif p == 'rh':
            pass
            

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~MAIN UI FUNCTIONS~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def disbaleindicate():
        homeicon_uns=ctk.CTkImage(Image.open('icons/home_uns.png'))
        home.configure(state='enabled',fg_color='#1e1e1e',text_color='#b6b6b6',image = homeicon_uns)
        transfer.configure(state='enabled',fg_color='#1e1e1e',text_color='#b6b6b6',image = transfericon)
        spending.configure(state='enabled',fg_color='#1e1e1e',text_color='#b6b6b6',image = spendingicon)
        credits.configure(state='enabled',fg_color='#1e1e1e',text_color='#b6b6b6',image = creditsicon)
        investing.configure(state='enabled',fg_color='#1e1e1e',text_color='#b6b6b6',image = investingicon)
        history.configure(state='enabled',fg_color='#1e1e1e',text_color='#b6b6b6',image = historyicon)
    
    def enablecategories():
        mobilebtn.configure(state='enabled',text_color='#b5b5b5',border_color='#2e2e2e')
        internetbtn.configure(state='enabled',text_color='#b5b5b5',border_color='#2e2e2e')
        transportbtn.configure(state='enabled',text_color='#b5b5b5',border_color='#2e2e2e')
        ewalletbtn.configure(state='enabled',text_color='#b5b5b5',border_color='#2e2e2e')
        govtbtn.configure(state='enabled',text_color='#b5b5b5',border_color='#2e2e2e')
        ottbtn.configure(state='enabled',text_color='#b5b5b5',border_color='#2e2e2e')
        gamesbtn.configure(state='enabled',text_color='#b5b5b5',border_color='#2e2e2e')
        travelbtn.configure(state='enabled',text_color='#b5b5b5',border_color='#2e2e2e')
        healthcarebtn.configure(state='enabled',text_color='#b5b5b5',border_color='#2e2e2e')
        grocerybtn.configure(state='enabled',text_color='#b5b5b5',border_color='#2e2e2e')
        educationbtn.configure(state='enabled',text_color='#b5b5b5',border_color='#2e2e2e')
        shoppingbtn.configure(state='enabled',text_color='#b5b5b5',border_color='#2e2e2e')

    def indicate(lb,page,type,value,image):
        if type == 'n' :
            disbaleindicate()
            newimg = ctk.CTkImage(Image.open(f'icons/{image}.png'))
            lb.configure(state='disabled',fg_color='#414141',text_color_disabled='white',image=newimg)
            switch_pages()
            page()
        elif type == 'c' :
            enablecategories()
            lb.configure(state = 'disabled',border_color='white',text_color_disabled='#ffffff')
            category_values(value)

    def category_values(currenttype):
        
        if len(payment_type) != 1:
            payment_type.append(currenttype)
        else:
            payment_type.pop(0)
            payment_type.append(currenttype)

    def switch_pages():
        for frame in mainframe.winfo_children():
            frame.destroy()

    def hover_more_in(dots) :
        dots.configure(text_color='#0096D9')
    
    def hover_more_out(dots) :
        dots.configure(text_color='#2e2e2e')

    def hover_back_in(e):
        newimg = ctk.CTkImage(Image.open(f'icons/back_sel.png'),size=(30,30))
        back.configure(image = newimg)

    def hover_back_out(e) :
        newimg = ctk.CTkImage(Image.open(f'icons/back.png'),size=(30,30))
        back.configure(image = newimg)

    def enter_recphone_entry(e):
        if rec_phnoStr.get() == 'Phone Number' or rec_phnoStr.get() == 'Enter valid phone no':
            rec_phnoStr.set('')
            transfer_to_entry.configure(text_color = 'white')
        
    def leave_recphone_entry(e):
        if rec_phnoStr.get() == '':
            rec_phnoStr.set('Phone Number')
            transfer_to_entry.configure(text_color = '#2e2e2e',textvariable=rec_phnoStr)
        else :
            pass

    def enter_recamt_entry(e):
        if rec_amtStr.get() == 'Amount, Rupees' or rec_amtStr.get() == 'Enter valid amount':
            rec_amtStr.set('')
            amount.configure(text_color = 'white')
        
    def leave_recamt_entry(e):
        if rec_amtStr.get() == '':
            rec_amtStr.set('Amount, Rupees')
            amount.configure(text_color = '#2e2e2e',textvariable=rec_amtStr)
        else :
            pass

    def to_upibox2(e):
        upipin_entry2.focus()
        upipin_entry1.configure(border_color='#2e2e2e')
        upipin_entry2.configure(border_color='#2e2e2e')
        upipin_entry3.configure(border_color='#2e2e2e')
        upipin_entry4.configure(border_color='#2e2e2e')
    
    def to_upibox3(e):
        upipin_entry3.focus()
    
    def to_upibox4(e):
        upipin_entry4.focus()

    def pmt_animation():

        global frames_delay

        gif_file = Image.open('MainUI/pmt_done1.gif')

        for r in range(0,gif_file.n_frames):

            gif_file.seek(r)
            gif_frames.append(gif_file.copy())

        frames_delay = gif_file.info['duration']
        play_pmt_animation()

    def play_pmt_animation():

        global frame_count, current_frame,pmt_gif

        if frame_count>= len(gif_frames)-1 :
            frame_count = -1
            play_pmt_animation()
        else:
            if not stop :
                frame_count+=1

                current_frame = ctk.CTkImage(gif_frames[frame_count],size=(400,300))
                pmt_gif.configure(image = current_frame)





                trnsctn_cmplt_frame.after(frames_delay,play_pmt_animation)

    def stop_pmt_animation():
        global stop 

        if stop:
            stop = False
        else:
            stop = True

    def back_to_trnsfr(e):
        try:
            stop_pmt_animation()
            trnsctn_cmplt_frame.destroy()
            transaction_details.clear()
            transferpage()
        except:
            pass

    def trnsctn_success(ramt,rphno):
        upipin_entry1.destroy()
        upipin_entry2.destroy()
        upipin_entry3.destroy()
        upipin_entry4.destroy()
        upi_proceed_btn.destroy()
        upi_label.destroy()
        upi_validation_label.destroy()

        pmt_status = ctk.CTkLabel(trnsctn_cmplt_frame,text="Success!",text_color="#0008ff",font=("Barlow SemiBold",55))
        pmt_status.place(x=650,y=280)
        receipt_amt = ctk.CTkLabel(trnsctn_cmplt_frame,text=f"₹ {ramt} was sent to {rphno}",text_color="#2e2e2e",font=("Barlow SemiBold",20))
        receipt_amt.place(x=630,y=360)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~MAIN UI~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    main = ctk.CTk()
    main.title("Nix")
    main.state("zoomed")
    main.wm_iconbitmap("NixIcon.ico")
    main.configure(fg_color='#161616')
    main.resizable(False,False)

    cursor.execute(f"SELECT ACCOUNT_NO,USERNAME FROM USER_DETAILS WHERE PHONE_NO = {currentuser[0]};")
    currentuser_accno = cursor.fetchone()
    currentuser.append(currentuser_accno[0])
    currentuser.append(currentuser_accno[1])

    mainframe=ctk.CTkFrame(main,fg_color='#161616')
    mainframe.place(x=0,y=0,relwidth=1,height=860)
    
    def homepage():
        home_frame=ctk.CTkFrame(mainframe,fg_color='#161616')
        home_frame.place(x=0,y=0,relwidth=1,relheight=1)

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~TOP BAR~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        wallet_label= ctk.CTkLabel(home_frame,text='Wallet',text_color="#2e2e2e",font=('Barlow Medium',15))
        wallet_label.place(x=24,y=26)
        wallet_line2=ctk.CTkLabel(home_frame,text='',bg_color='#2e2e2e')
        wallet_line2.place(x=22,y=55,width=591,height=2)
        global wallet_more
        wallet_more = ctk.CTkLabel(home_frame,text='●●●',text_color='#2e2e2e')
        wallet_more.place(x=458,y=26)
        
        wallet_more.bind('<Enter>',hover_more_in(wallet_more))
        wallet_more.bind('<Leave>',hover_more_out(wallet_more))

        sts_label= ctk.CTkLabel(home_frame,text='Safe to Spend',text_color="#2e2e2e",font=('Barlow Medium',15))
        sts_label.place(x=531,y=26)
        sts_line2=ctk.CTkLabel(home_frame,text='',bg_color='#2e2e2e')
        sts_line2.place(x=530,y=55,width=593,height=2)
        global sts_more
        sts_more = ctk.CTkLabel(home_frame,text='●●●',text_color='#2e2e2e')
        sts_more.place(x=968,y=26)

        sts_more.bind('<Enter>',hover_more_in(sts_more))
        sts_more.bind('<Leave>',hover_more_out(sts_more))

        ub_label= ctk.CTkLabel(home_frame,text='Upcoming Bills',text_color="#2e2e2e",font=('Barlow Medium',15))
        ub_label.place(x=1042,y=26)
        ub_line2=ctk.CTkLabel(home_frame,text='',bg_color='#2e2e2e')
        ub_line2.place(x=1041,y=55,width=591,height=2)
        global ub_more
        ub_more = ctk.CTkLabel(home_frame,text='●●●',text_color='#2e2e2e')
        ub_more.place(x=1476,y=26)

        ub_more.bind('<Enter>',hover_more_in(ub_more))
        ub_more.bind('<Leave>',hover_more_out(ub_more))

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~WALLET~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        global ecard
        ecard = Image.open('Cards/Rebranded Nix Card.png')
        ecard = ecard.resize((571,331))
        ecard.save('Cards/Rebranded Nix Card.png')
        ecard = PhotoImage(file='Cards/Rebranded Nix Card.png')
        c = ctk.CTkCanvas(home_frame,width=570,height=329,bg='#161616',bd=0,highlightthickness=0,relief='ridge')
        c.place(x=33,y=96)

        c.create_image(0,0,image=ecard,anchor='nw')

        ecard_details()

        currencies = {'india':'R  U  P  E  E','usa':'U  S  D','aus':'A  U  D','canada':'C  A  D','china':'C  N  Y','czech':'C  Z  K','euro':'E  U  R','japan':'J  P  Y','singapore':'S  G  D','france':'C  H  F','vietnam':'V  N  D','uae':'A  E  D'}
        sel_currency = ctk.StringVar()
        sel_currency.set(currencies['india'])

        c.create_text(193,140,text=f'₹ {balance}',font=('Barlow Medium',60),fill='#6C7076')
        c.create_text(135,43,text=sel_currency.get() ,font=('Barlow Bold',16),fill='#6C7076',anchor='e')
        c.create_text(230,250,text=censored_cardno,font=('Barlow SemiBold',20),fill='#6C7076',anchor='e')
        c.create_text(445,250,text=expdate,font=('Barlow SemiBold',20),fill='#6C7076',anchor='e')

        card_slide  = ctk.CTkLabel(home_frame,text='●',text_color='#0096D9')
        card_slide.place(x=255,y=345)

        

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~SEND MONEY~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        trnsct_label = ctk.CTkLabel(home_frame,text='Send Money',text_color='#2e2e2e',bg_color='#161616',font=('Barlow Medium',15))
        trnsct_label.place(x=221,y=377)
        trnsct_line=ctk.CTkLabel(home_frame,text='',bg_color='#2e2e2e')
        trnsct_line.place(x=22,y=410,width=591,height=2)
        

        s = ctk.CTkCanvas(home_frame,width=590,height=79,bg='#161616',bd=0,highlightthickness=0,relief='ridge',scrollregion = (0,0,3000,0))
        s.place(x=28,y=518)

        

        s.bind('<MouseWheel>',lambda event: s.xview_scroll(-int(event.delta / 10),"units"))

        trnsct_tag = ctk.CTkLabel(home_frame,text='   Recent   ',height=20,fg_color='#2e2e2e',bg_color='#161616',font=('Barlow',10),text_color='#b6b6b6')
        trnsct_tag.place(x=22,y=412)


        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~RECENT OPERATIONS~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        recent_label = ctk.CTkLabel(home_frame,text='Recent Operations',text_color='#2e2e2e',bg_color='#161616',font=('Barlow Medium',15))
        recent_label.place(x=24,y=500)
        recent_line = ctk.CTkLabel(home_frame,text='',bg_color='#2e2e2e')
        recent_line.place(x=22,y=530,width=591,height=2)

        cursor.execute(f"SELECT TO_NAME,FROM_NAME,AMOUNT FROM TRANSACTIONS WHERE FROM_NAME = '{currentuser[2]}' OR TO_NAME = '{currentuser[2]}' ORDER BY DATE DESC")
        recent_opsd = cursor.fetchmany(10)
        item_number = len(recent_opsd)
        list_height = item_number * 150

        recentops = ctk.CTkCanvas(home_frame,bg = '#161616',scrollregion = (0,0,1000,list_height),width=589,height=160,bd=0,highlightthickness=0,relief='ridge')
        recentops.place(x=30,y=693)

        global recentops_frame
        recentops_frame = ctk.CTkFrame(recentops,fg_color='red',height=list_height,width=1000)
        # recentops_frame.place(x=0,y=0,relwidth=1,relheight=1)
        recentops.create_window(34,656,window=recentops_frame)

        if recent_opsd != ['1']:
            pass
        else:
            ro_status = ctk.CTkLabel(recentops_frame,text="All your transactions\nwill be shown here",text_color="#2e2e2e",font=("Barlow SemiBold",13))
            ro_status.place(x=50,y=650)















        recentops.bind('<MouseWheel>',lambda event: recentops.yview_scroll(-int(event.delta / 10),"units"))
        
        recent_tag = ctk.CTkLabel(home_frame,text='   Today   ',height=20,fg_color='#2e2e2e',bg_color='#161616',font=('Barlow',10),text_color='#b6b6b6')
        recent_tag.place(x=22,y=532)

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~EXPENSES~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        expenses_label = ctk.CTkLabel(home_frame,text='Expenses',text_color='#0096D9',bg_color='#161616',font=('Barlow Medium',15))
        expenses_label.place(x=617,y=285)

        income_label = ctk.CTkLabel(home_frame,text='Income',text_color='#2e2e2e',bg_color='#161616',font=('Barlow Medium',15))
        income_label.place(x=864,y=285)

        expenses_line=ctk.CTkLabel(home_frame,text='',bg_color='#2e2e2e')
        expenses_line.place(x=530,y=315,width=593,height=2)
        
        selection_line=ctk.CTkLabel(home_frame,text='',bg_color='#0096D9')
        selection_line.place(x=530,y=315,width=296,height=2)


        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~MY GOALS~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        mg_label = ctk.CTkLabel(home_frame,text='My Goals',text_color='#2e2e2e',bg_color='#161616',font=('Barlow Medium',15))
        mg_label.place(x=533,y=515)
        
        mg_line=ctk.CTkLabel(home_frame,text='',bg_color='#2e2e2e')
        mg_line.place(x=530,y=545,width=593,height=2)
    
    def transferpage():
        transfer_frame = ctk.CTkFrame(mainframe,fg_color='#161616')
        transfer_frame.place(x=0,y=0,relwidth=1,relheight=1)

        smoney_label= ctk.CTkLabel(transfer_frame,text='Send Money',text_color="#2e2e2e",font=('Barlow Medium',15))
        smoney_label.place(x=21,y=26)
        smoney_line=ctk.CTkLabel(transfer_frame,text='',bg_color='#2e2e2e',height=1)
        smoney_line.place(x=18,y=55,width=580,height=2)


        transferlabel=ctk.CTkLabel(transfer_frame,text='Transfer',text_color="#2e2e2e",font=('Barlow Medium',15))
        transferlabel.place(x=521,y=26)
        transferline=ctk.CTkLabel(transfer_frame,text='',bg_color='#2e2e2e',height=1)
        transferline.place(x=518,y=55,width=623,height=2)


        categorylabel= ctk.CTkLabel(transfer_frame,text='Category',text_color="#2e2e2e",font=('Barlow Medium',15))
        categorylabel.place(x=1056,y=26)
        categoryline=ctk.CTkLabel(transfer_frame,text='',bg_color='#2e2e2e',height=1)
        categoryline.place(x=1053,y=55,width=582,height=2)

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~SEND MONEY COLUMN~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        select_from_email = ctk.CTkEntry(transfer_frame,
                                         placeholder_text='Enter Email',placeholder_text_color='#2e2e2e',
                                         border_width=2,border_color='#2e2e2e',
                                         bg_color='#161616',fg_color='#161616',corner_radius=18,
                                         text_color='white',font=('Barlow Medium',13),
                                         height=55,width=460)
        select_from_email.place(x=21,y=93)
                                         
        or_label = ctk.CTkLabel(transfer_frame,text='or choose from list',text_color='#2e2e2e',font=('Barlow Medium',14))
        or_label.place(x=200,y=160)

        contents_label = ctk.CTkLabel(transfer_frame,
                                      text='Contents',text_color='#2e2e2e',font=('Barlow Medium',15),)
        contents_label.place(x=21,y=208)
        contents_line=ctk.CTkLabel(transfer_frame,text='',bg_color='#2e2e2e',height=1)
        contents_line.place(x=18,y=242,width=580,height=2)

        contacts_list = ctk.CTkCanvas(transfer_frame,width=580,height=520,bg='#161616',bd=0,highlightthickness=0,relief='ridge',scrollregion = (0,0,1000,6000))
        contacts_list.place(x=24,y=325)

        contacts_list.create_line(0,0,1000,6000,fill='red',width=10)
        contacts_list.place(x=24,y=325)

        contacts_list.bind('<MouseWheel>',lambda event: contacts_list.yview_scroll(-int(event.delta / 10),"units"))



        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~TRANSFER COLUMN~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        from_label = ctk.CTkLabel(transfer_frame,text = 'From',text_color='#2e2e2e',font=('Barlow Medium',15))
        from_label.place(x=521,y=63)
        
        
        cursor.execute(f'SELECT ACCOUNT_DETAILS.CARD_NO FROM USER_DETAILS,ACCOUNT_DETAILS WHERE USER_DETAILS.ACCOUNT_NO = ACCOUNT_DETAILS.ACCOUNT_NO AND USER_DETAILS.PHONE_NO = {currentuser[0]};')
        transfer_card_values = cursor.fetchone()

        cursor.execute(f'SELECT BALANCE FROM ACCOUNT_DETAILS WHERE CARD_NO = {transfer_card_values[0]};')
        transfer_balance_values = cursor.fetchone()
        card_value = ctk.StringVar(transfer_frame,f'Nix Master Card - ●●●● {str(transfer_card_values[0])[8:]}')
        balance_value = ctk.StringVar(transfer_frame,f'₹{transfer_balance_values[0]}')

        global transfer_from_entry
        transfer_from_entry = ctk.CTkEntry(transfer_frame,
                                              textvariable=balance_value,
                                              placeholder_text_color= '#2e2e2e',
                                              text_color='#3f3f3f',
                                              border_color='#2e2e2e',border_width=2,
                                              fg_color='#161616',
                                              corner_radius=18,
                                              bg_color='#161616',
                                              height=55,width=495,
                                              font=('Barlow Medium',13),
                                              state= DISABLED
                                              )
        transfer_from_entry.place(x=521,y=93)
        transfer_from_status = ctk.CTkLabel(transfer_frame,textvariable = card_value,text_color='#2e2e2e',font=('Barlow Regular',11),fg_color='#161616')
        transfer_from_status.place(x=840,y=94)

        to_label = ctk.CTkLabel(transfer_frame,text = 'To',text_color='#2e2e2e',font=('Barlow Medium',15))
        to_label.place(x=521,y=160)

        global transfer_to_entry
        global rec_phnoStr
        rec_phnoStr = ctk.StringVar()
        rec_phnoStr.set('Phone Number')
        transfer_to_entry = ctk.CTkEntry(transfer_frame,
                                              placeholder_text= 'Phone Number',
                                              placeholder_text_color= '#2e2e2e',
                                              textvariable=rec_phnoStr,
                                              text_color='#2e2e2e',
                                              border_color='#2e2e2e',border_width=2,
                                              fg_color='#161616',
                                              corner_radius=18,
                                              bg_color='#161616',
                                              height=55,width=495,
                                              font=('Barlow Medium',13)
                                              )
        transfer_to_entry.place(x=521,y=190)

        transfer_to_entry.bind('<FocusIn>',enter_recphone_entry)
        transfer_to_entry.bind('<FocusOut>',leave_recphone_entry)

        
        global amount
        global rec_amtStr
        rec_amtStr = ctk.StringVar()
        rec_amtStr.set('Amount, Rupees')
        amount = ctk.CTkEntry(transfer_frame,
                                placeholder_text= 'Amount, Rupees',
                                textvariable=rec_amtStr,
                                placeholder_text_color= '#2e2e2e',
                                text_color='#2e2e2e',
                                border_color='#2e2e2e',border_width=2,
                                fg_color='#161616',
                                corner_radius=18,
                                bg_color='#161616',
                                height=55,width=495,
                                font=('Barlow Medium',13)
                                )
        amount.place(x=521,y=280)

        amount.bind('<FocusIn>',enter_recamt_entry)
        amount.bind('<FocusOut>',leave_recamt_entry)

        
        pay_amount_btn = ctk.CTkButton(transfer_frame,
                                       text = 'Transfer Money',
                                       corner_radius=18,
                                       height=60,
                                       fg_color="#0008ff",
                                       text_color="#ffffff",
                                       width=260,
                                       hover_color='#001952',
                                       command=payment_gateway)
        pay_amount_btn.place(x=750,y=380)

        global validation_var
        validation_var = ctk.StringVar()
        validation_label = ctk.CTkLabel(transfer_frame,textvariable=validation_var,text_color="#C21807",font=('Barlow Medium',14))
        validation_label.place(x=540,y=395)

        ctcicon=ctk.CTkImage(Image.open('icons/cardtocard.png'),size=(43,43))
        cardtocard_pmts = ctk.CTkButton(transfer_frame,
                                        text='From card to card',text_color='#b5b5b5',font=('Barlow Medium',13),
                                        image=ctcicon,compound=LEFT,anchor='w',corner_radius=18,hover='disable',
                                        fg_color='#161616',border_width=2,border_color='#2e2e2e',
                                        height=75,width=495,
                                        state='disabled')
        cardtocard_pmts.place(x=521,y=480)

        inticon=ctk.CTkImage(Image.open('icons/international.png'),size=(43,43))
        int_pmts = ctk.CTkButton(transfer_frame,
                                        text='International Payments',text_color='#b5b5b5',font=('Barlow Medium',13),
                                        image=inticon,compound=LEFT,anchor='w',corner_radius=18,hover='disable',
                                        fg_color='#161616',border_width=2,border_color='#2e2e2e',
                                        height=75,width=495,
                                        state='disabled')
        int_pmts.place(x=521,y=575)

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~CATEGORIES~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        global payment_type
        payment_type = []

        global mobilebtn
        mobileicon=ctk.CTkImage(Image.open('category_icons/smartphone.png'),size=(43,43))
        mobilebtn = ctk.CTkButton(transfer_frame,height=130,width=120,
                                  fg_color='#161616',border_width=2,border_color='#2e2e2e',
                                  text='Mobile\nBills',font=('Barlow Medium',13),text_color='#b5b5b5',
                                  corner_radius=18,hover='disable',
                                  image=mobileicon,compound=TOP,
                                  command = lambda : indicate(mobilebtn,None,'c','mobile',None))
        mobilebtn.place(x=1056+15,y = 85)

        global internetbtn
        interneticon=ctk.CTkImage(Image.open('category_icons/internet.png'),size=(43,43))
        internetbtn = ctk.CTkButton(transfer_frame,height=130,width=120,
                                  fg_color='#161616',border_width=2,border_color='#2e2e2e',
                                  text='Internet &\nSubscriptions',font=('Barlow Medium',12),text_color='#b5b5b5',
                                  corner_radius=18,hover='disable',
                                  image=interneticon,compound=TOP,
                                  command = lambda : indicate(internetbtn,None,'c','internet',None))
        internetbtn.place(x=1056+15,y = 235)
        
        global transportbtn
        transporticon=ctk.CTkImage(Image.open('category_icons/transport.png'),size=(43,43))
        transportbtn = ctk.CTkButton(transfer_frame,height=130,width=120,
                                  fg_color='#161616',border_width=2,border_color='#2e2e2e',
                                  text='Transport',font=('Barlow Medium',13),text_color='#b5b5b5',
                                  corner_radius=18,hover='disable',
                                  image=transporticon,compound=TOP,
                                  command = lambda : indicate(transportbtn,None,'c','transport',None))
        transportbtn.place(x=1056+15,y = 385)
        
        global ewalletbtn
        ewalleticon=ctk.CTkImage(Image.open('category_icons/ewallet.png'),size=(43,43))
        ewalletbtn = ctk.CTkButton(transfer_frame,height=130,width=120,
                                  fg_color='#161616',border_width=2,border_color='#2e2e2e',
                                  text='E-wallets',font=('Barlow Medium',13),text_color='#b5b5b5',
                                  corner_radius=18,hover='disable',
                                  image=ewalleticon,compound=TOP,
                                  command = lambda : indicate(ewalletbtn,None,'c','ewallet',None))
        ewalletbtn.place(x=1056+15,y = 535)
        
        global govtbtn
        govticon=ctk.CTkImage(Image.open('category_icons/govt.png'),size=(43,43))
        govtbtn = ctk.CTkButton(transfer_frame,height=130,width=120,
                                  fg_color='#161616',border_width=2,border_color='#2e2e2e',
                                  text='Govt\nBills',font=('Barlow Medium',13),text_color='#b5b5b5',
                                  corner_radius=18,hover='disable',
                                  image=govticon,compound=TOP,
                                  command = lambda : indicate(govtbtn,None,'c','govt',None))
        govtbtn.place(x=1206+15,y = 85)
        
        global ottbtn
        otticon=ctk.CTkImage(Image.open('category_icons/ott.png'),size=(43,43))
        ottbtn = ctk.CTkButton(transfer_frame,height=130,width=120,
                                  fg_color='#161616',border_width=2,border_color='#2e2e2e',
                                  text='OTT\nSubscriptions',font=('Barlow Medium',12),text_color='#b5b5b5',
                                  corner_radius=18,hover='disable',
                                  image=otticon,compound=TOP,
                                  command = lambda : indicate(ottbtn,None,'c','ott',None))
        ottbtn.place(x=1206+15,y = 235)
        
        global gamesbtn
        gamesicon=ctk.CTkImage(Image.open('category_icons/games.png'),size=(43,43))
        gamesbtn = ctk.CTkButton(transfer_frame,height=130,width=120,
                                  fg_color='#161616',border_width=2,border_color='#2e2e2e',
                                  text='Games',font=('Barlow Medium',13),text_color='#b5b5b5',
                                  corner_radius=18,hover='disable',
                                  image=gamesicon,compound=TOP,
                                  command = lambda : indicate(gamesbtn,None,'c','games',None))
        gamesbtn.place(x=1206+15,y = 385)
        
        global travelbtn
        travelicon=ctk.CTkImage(Image.open('category_icons/travel.png'),size=(43,43))
        travelbtn = ctk.CTkButton(transfer_frame,height=130,width=120,
                                  fg_color='#161616',border_width=2,border_color='#2e2e2e',
                                  text='Travelling',font=('Barlow Medium',13),text_color='#b5b5b5',
                                  corner_radius=18,hover='disable',
                                  image=travelicon,compound=TOP,
                                  command = lambda : indicate(travelbtn,None,'c','travel',None))
        travelbtn.place(x=1206+15,y = 535)
        
        global healthcarebtn
        healthcareicon=ctk.CTkImage(Image.open('category_icons/healthcare.png'),size=(43,43))
        healthcarebtn = ctk.CTkButton(transfer_frame,height=130,width=120,
                                  fg_color='#161616',border_width=2,border_color='#2e2e2e',
                                  text='Healthcare &\nMedicines',font=('Barlow Medium',12),text_color='#b5b5b5',
                                  corner_radius=18,hover='disable',
                                  image=healthcareicon,compound=TOP,
                                  command = lambda : indicate(healthcarebtn,None,'c','healthcare',None))
        healthcarebtn.place(x=1356+15,y = 85)
        
        global grocerybtn
        groceryicon=ctk.CTkImage(Image.open('category_icons/grocery.png'),size=(43,43))
        grocerybtn = ctk.CTkButton(transfer_frame,height=130,width=120,
                                  fg_color='#161616',border_width=2,border_color='#2e2e2e',
                                  text='Grocery',font=('Barlow Medium',12),text_color='#b5b5b5',
                                  corner_radius=18,hover='disable',
                                  image=groceryicon,compound=TOP,
                                  command = lambda : indicate(grocerybtn,None,'c','grocery',None))
        grocerybtn.place(x=1356+15,y = 235)
        
        global educationbtn
        educationicon=ctk.CTkImage(Image.open('category_icons/education.png'),size=(43,43))
        educationbtn = ctk.CTkButton(transfer_frame,height=130,width=120,
                                  fg_color='#161616',border_width=2,border_color='#2e2e2e',
                                  text='Education',font=('Barlow Medium',13),text_color='#b5b5b5',
                                  corner_radius=18,hover='disable',
                                  image=educationicon,compound=TOP,
                                  command = lambda : indicate(educationbtn,None,'c','education',None))
        educationbtn.place(x=1356+15,y = 385)
        
        global shoppingbtn
        shoppingicon=ctk.CTkImage(Image.open('category_icons/shopping.png'),size=(43,43))
        shoppingbtn = ctk.CTkButton(transfer_frame,height=130,width=120,
                                  fg_color='#161616',border_width=2,border_color='#2e2e2e',
                                  text='Shopping &\nLuxe',font=('Barlow Medium',13),text_color='#b5b5b5',
                                  corner_radius=18,hover='disable',
                                  image=shoppingicon,compound=TOP,
                                  command = lambda : indicate(shoppingbtn,None,'c','shopping',None))
        shoppingbtn.place(x=1356+15,y = 535)
    
    def spendingpage():
        spending_frame = ctk.CTkFrame(mainframe,fg_color='#161616')
        spending_frame.place(x=0,y=0,relwidth=1,relheight=1)

        label = ctk.CTkLabel(spending_frame,text='150 rupay dega!')
        label.pack()
    
    def creditspage():
        credits_frame = ctk.CTkFrame(mainframe,fg_color='#161616')
        credits_frame.place(x=0,y=0,relwidth=1,relheight=1)

    def investingpage():
        investing_frame = ctk.CTkFrame(mainframe,fg_color='#161616')
        investing_frame.place(x=0,y=0,relwidth=1,relheight=1)
    
    def historypage():
        def updatesize(e):
            if list_height >= history_frame.winfo_height():
                pass
            else:
                historylist.unbind_all('<MouseWheel>')

            historylist.create_window((0,0),window=historydetailframe
                                      ,width=history_frame.winfo_width()
                                      ,height=list_height,anchor='nw')


        cursor.execute(f"SELECT * FROM TRANSACTIONS WHERE FROM_ACCNO = {currentuser[1]} OR TO_ACCNO = {currentuser[1]} ;")
        historydetails = cursor.fetchall()
        item_number = len(historydetails)
        list_height = item_number * 150

        global history_frame
        history_frame = ctk.CTkFrame(mainframe,fg_color='#161616')
        history_frame.place(x=0,y=0,relwidth=1,relheight=1)

        hstry_title = ctk.CTkLabel(history_frame,text="All Transactions",text_color="#2e2e2e",font=("Barlow SemiBold",35))
        hstry_title.pack(pady=10,anchor='center')
        
        if historydetails != []:
            historylist = ctk.CTkCanvas(history_frame,bg='#161616',bd=0,highlightthickness=0,relief='ridge',scrollregion = (0,0,history_frame.winfo_width(),list_height))
            historylist.pack(pady=10,anchor='center',expand=True,fill='both')

            #Display Frame
            global historydetailframe
            historydetailframe = ctk.CTkFrame(history_frame,fg_color='#161616',bg_color='#161616')

            for index,item in enumerate(historydetails):
                create_history(item,'hp').pack(expand = True, fill='both',padx=10,pady=5,side=BOTTOM)

            historylist.bind_all('<MouseWheel>',lambda event: historylist.yview_scroll(-int(event.delta / 40),"units"))
            history_frame.bind('<Configure>', updatesize)
        
        else:
            hstry_status = ctk.CTkLabel(history_frame,text="All your transactions\nwill be shown here",text_color="#2e2e2e",font=("Barlow SemiBold",25))
            hstry_status.place(x=655,y=300)
    
    def settingspage():
        settings_frame = ctk.CTkFrame(mainframe,fg_color='#161616')
        settings_frame.place(x=0,y=0,relwidth=1,relheight=1)

    def upi_transaction_page():
        global trnsctn_cmplt_frame
        trnsctn_cmplt_frame = ctk.CTkFrame(mainframe,fg_color='#161616')
        trnsctn_cmplt_frame.place(x=0,y=0,relwidth=1,relheight=1)


        nixlogo = ctk.CTkImage(Image.open('LoginWindow/NixIcon.png'),size=(75,75))
        l1 = ctk.CTkLabel(trnsctn_cmplt_frame,text="",image=nixlogo,bg_color="#161616")
        l1.pack(anchor='ne',padx=15,pady=15)

        nixlogo2 = ctk.CTkImage(Image.open('LoginWindow/Nix Logo 2.png'),size=(75, 53))
        l2 = ctk.CTkLabel(trnsctn_cmplt_frame,text="",image=nixlogo2,bg_color="#161616")
        l2.place(x=15,y=30)

        global back
        backicon=ctk.CTkImage(Image.open('icons/back.png'),size=(30,30))
        back = ctk.CTkLabel(trnsctn_cmplt_frame,text="",image=backicon)
        back.place(x=30,y=100)

        back.bind('<Enter>',hover_back_in)
        back.bind('<Leave>',hover_back_out)
        back.bind('<Button-1>',back_to_trnsfr)


        global pmt_gif
        pmt_gif = ctk.CTkLabel(trnsctn_cmplt_frame,text="")
        pmt_gif.place(x=560,y=30)

        threading.Thread(target=pmt_animation).start()



        global upi_label
        upi_label = ctk.CTkLabel(trnsctn_cmplt_frame,text='E n t e r   U  P  I   P i n',text_color='#2e2e2e',
                                 font=('Barlow SemiBold',20))
        upi_label.place(x=603,y=304)

        global upipin_entry1
        upipin_entry1 = ctk.CTkEntry(trnsctn_cmplt_frame,border_color='#2e2e2e',border_width=2,
                                     text_color='white',font=('Barlow Medium',20),
                                     corner_radius=15,width=70,height=90,show = "●",
                                     fg_color='#161616',bg_color='#161616',justify='center')
        upipin_entry1.place(x=521+75,y=340)
        upipin_entry1.bind('<Key>',to_upibox2)
        
        global upipin_entry2
        upipin_entry2 = ctk.CTkEntry(trnsctn_cmplt_frame,border_color='#2e2e2e',border_width=2,
                                     text_color='white',font=('Barlow Medium',20),
                                     corner_radius=15,width=70,height=90,show = "●",
                                     fg_color='#161616',bg_color='#161616',justify='center')
        upipin_entry2.place(x=611+75,y=340)
        upipin_entry2.bind('<Key>',to_upibox3)
        
        global upipin_entry3
        upipin_entry3 = ctk.CTkEntry(trnsctn_cmplt_frame,border_color='#2e2e2e',border_width=2,
                                     text_color='white',font=('Barlow Medium',20),
                                     corner_radius=15,width=70,height=90,show = "●",
                                     fg_color='#161616',bg_color='#161616',justify='center')
        upipin_entry3.place(x=701+75,y=340)
        upipin_entry3.bind('<Key>',to_upibox4)
        
        global upipin_entry4
        upipin_entry4 = ctk.CTkEntry(trnsctn_cmplt_frame,border_color='#2e2e2e',border_width=2,
                                     text_color='white',font=('Barlow Medium',20),
                                     corner_radius=15,width=70,height=90,show = "●",
                                     fg_color='#161616',bg_color='#161616',justify='center')
        upipin_entry4.place(x=791+75,y=340)

        global upi_proceed_btn
        upi_proceed_btn = ctk.CTkButton(trnsctn_cmplt_frame,
                                       text = 'Pay',
                                       corner_radius=15,
                                       height=60,
                                       fg_color="#0008ff",
                                       hover_color="#001952",
                                       text_color="white",
                                       width=340,
                                       anchor='center',
                                       command=upi_pin_verification)
        upi_proceed_btn.place(x=596,y=450)

        global upi_valid_var
        global upi_validation_label
        upi_valid_var = ctk.StringVar()
        upi_validation_label = ctk.CTkLabel(trnsctn_cmplt_frame,textvariable = upi_valid_var,
                                            font=('Barlow Medium',15),text_color='red')
        upi_validation_label.place(x=598,y=520)


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~NAVBAR~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    navbar = ctk.CTkFrame(main,bg_color='#161616',fg_color='#252525',corner_radius=26,width=1492,height=85)
    navbar.place(x=21+1,y=688)

    
    homeicon=ctk.CTkImage(Image.open('icons/home.png'))
    home = ctk.CTkButton(main,text='Home',state='disabled',image=homeicon,compound='top',font=('Barlow Medium',10),width=65,height=65,bg_color='#252525',text_color='white',fg_color='#414141',border_width=0,corner_radius=12,hover_color='#1e1e1e',command=lambda : indicate(home, homepage,'n',None,'home'))
    home.place(x=533+1,y=699)

    
    transfericon=ctk.CTkImage(Image.open('icons/transfer_uns.png'))
    transfer = ctk.CTkButton(main,text='Transfer',image=transfericon,compound='top',font=('Barlow Medium',10),width=65,height=65,bg_color='#252525',text_color='#b6b6b6',fg_color='#1e1e1e',border_width=0,corner_radius=12,hover_color='#1e1e1e',command=lambda : indicate(transfer,transferpage,'n',None,'transfer'))
    transfer.place(x=612+1,y=699)

    
    spendingicon=ctk.CTkImage(Image.open('icons/spending_uns.png'))
    spending = ctk.CTkButton(main,text='Spending',image=spendingicon,compound='top',font=('Barlow Medium',10),width=65,height=65,bg_color='#252525',text_color='#b6b6b6',fg_color='#1e1e1e',border_width=0,corner_radius=12,hover_color='#1e1e1e',command=lambda : indicate(spending,spendingpage,'n',None,'spending'))
    spending.place(x=691+1,y=699)

    
    creditsicon=ctk.CTkImage(Image.open('icons/credits_uns.png'))
    credits = ctk.CTkButton(main,text='Nix Area',image=creditsicon,compound='top',font=('Barlow Medium',10),width=65,height=65,bg_color='#252525',text_color='#b6b6b6',fg_color='#1e1e1e',border_width=0,corner_radius=12,hover_color='#1e1e1e',command=lambda : indicate(credits,creditspage,'n',None,'credits'))
    credits.place(x=771+1,y=699)

    
    investingicon=ctk.CTkImage(Image.open('icons/investing_uns.png'))
    investing = ctk.CTkButton(main,text='Investing',image=investingicon,compound='top',font=('Barlow Medium',10),width=65,height=65,bg_color='#252525',text_color='#b6b6b6',fg_color='#1e1e1e',border_width=0,corner_radius=12,hover_color='#1e1e1e',command=lambda : indicate(investing,investingpage,'n',None,'investing'))
    investing.place(x=850+1,y=699)

    
    historyicon=ctk.CTkImage(Image.open('icons/history_uns.png'))
    history = ctk.CTkButton(main,text='History',image=historyicon,compound='top',font=('Barlow Medium',10),width=65,height=65,bg_color='#252525',text_color='#b6b6b6',fg_color='#1e1e1e',border_width=0,corner_radius=12,hover_color='#1e1e1e',command=lambda : indicate(history,historypage,'n',None,'history'))
    history.place(x=929+1,y=699)

    settingsicon=ctk.CTkImage(Image.open('icons/settings2.png'))
    settings = ctk.CTkLabel(main,text='',image=settingsicon,font=('Barlow Medium',10),height=65,bg_color='#252525',fg_color='#252525')
    settings.place(x=1410,y=699)
    
    notificationicon=ctk.CTkImage(Image.open('icons/notification1.png'))
    notification = ctk.CTkLabel(main,text='',image=notificationicon,font=('Barlow Medium',10),height=65,bg_color='#252525',fg_color='#252525')
    notification.place(x=1360,y=699)









    
    homepage()
    main.mainloop()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Main~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
if __name__ == '__main__' :
    splashScreen()
