import smtplib
from misc import *

# Import the email modules we'll need
from config import *
from email.mime.text import MIMEText
from smtplib import SMTPException



def sendEmail(progress,total):
    msg = "\r\n".join([
      "From: info@company.com",
      "To: you",
      "Subject: PUSH NOTIFICATION UPDATES",
      "",
      "Notification progress %d,%d"% (progress,total)
      ])
    
    try:
        smtpObj = smtplib.SMTP('smtp.gmail.com:587')
        smtpObj.ehlo()
        smtpObj.starttls()
        smtpObj.login(EMAIL_ADDRESS,EMAIL_PASSWORD)
        smtpObj.sendmail(sender, receivers, msg)         
        print "Successfully sent email"
        logger.info("Successfully sent email")
    except SMTPException:
        logger.info("Error: unable to send email")
        print "Error: unable to send email"

def sendCustomEmail(subject,message):
    msg = "\r\n".join([
      "From: info@company.com",
      "To: you",
      "Subject: PUSH NOTIFICATION "+subject,
      "",
      " "+message
      ])
    
    try:
        smtpObj = smtplib.SMTP('smtp.gmail.com:587')
        smtpObj.ehlo()
        smtpObj.starttls()
        smtpObj.login(EMAIL_ADDRESS,EMAIL_PASSWORD)
        smtpObj.sendmail(sender, receivers, msg)         
    except SMTPException:
        logger.info("Error: unable to send email")
        print "Error: unable to send email"
        
        
if __name__=="__main__":
    for i in range(1,10000):
        if i % 1000==0:
            sendEmail(i,10000)
    sendEmail(i,10000)