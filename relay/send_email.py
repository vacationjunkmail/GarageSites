#!/usr/bin/env python3
import configparser
from os.path import expanduser

#https://yuji.wordpress.com/2011/06/22/python-imaplib-imap-example-with-gmail/
#http://www.vineetdhanawat.com/blog/2012/06/how-to-extract-email-gmail-contents-as-text-using-imaplib-via-imap-in-python-3/

#https://stackabuse.com/how-to-send-emails-with-gmail-using-python/
#Code below
import smtplib
import email

def read_config_file(filename = '.my.cnf', section = 'email'):
    parser = configparser.ConfigParser()
    #config_file = "{}/{}".format(expanduser("~"),filename)
    config_file = "/home/pi/{}".format(filename)
    #print(config_file)
    parser.read(config_file,encoding = "utf-8")
    
    data = {}
    if parser.has_section(section):
        items = parser.items(section)
        for item in items:
            data[item[0]] = item[1]
    else:
        raise Exception("{0} not found in {1}".format(section,config_file))
    return data

#f = read_config_file()
#print(f)

class gmail_connection():        
    def __init__(self):
        self.email_config = read_config_file()
        try:
            self.user = self.email_config['user']
            self.pwd = self.email_config['password']
            self.server = smtplib.SMTP_SSL('smtp.gmail.com',465)
            self.server.ehlo()
            self.server.login(self.user,self.pwd)
            print("Message sent")
        except Exception as e:
            print("Somthing happened...\n\t{}".format(e))

    def send_pwd(self,toaddr,data):
        msg = ("Subject:Your Garage Password.\r\nYour password is\n{}".format(data))
        self.server.sendmail(self.user,toaddr,msg)

        return ""

    def close_gmail(self):
        try:
            self.server.close()
            show_msg = "Email Closed Successfully."
        except Exception as e:
            show_msg = "Something happened...\n\t".format(e)
        return show_msg
