import smtplib




def prompt(prompt):
    return input(prompt).strip()

fromaddr = "gurunathrajagopal@gmail.com"
toaddrs  = "rajagurunath5@gmail.com"
print( "Enter message, end with ^D (Unix) or ^Z (Windows):")

# Add the From: and To: headers at the start!
msg = ("From: %s\r\nTo: %s\r\n\r\n"
       % (fromaddr, ", ".join(toaddrs)))
while 1:
    try:
        line = input()
    except EOFError:
        break
    if not line:
        break
    msg = msg + line

print ("Message length is " + repr(len(msg)))

server = smtplib.SMTP('192.168.43.192')
server.set_debuglevel(1)
server.sendmail(fromaddr, toaddrs, msg)
server.quit()
