# Keylogging and Encryption Utility

## Overview

This project is a keylogging and encryption tool that captures system details, user keystrokes, audio recordings, and screenshots. The captured data is encrypted using Fernet encryption and can be sent via email. The project also includes decryption functionality to retrieve the original data.

## Features

1. Keylogging
   - Captures all keystrokes and logs them.
   - Stores log data in e_key_log.txt (encrypted format).

2. System Information Logging
   - Records system information such as OS details, IP address, and machine details.
   - Stores log data in e_sys_details.txt (encrypted format).

3. Audio Recording
   - Records 5 seconds of audio from the microphone.
   - Encrypts and stores it locally before sending it via email.

4. Screenshot Capture
   - Captures the user's screen and saves the image.
   - Encrypts and emails the screenshot to a specified email address.

5. Encryption & Decryption
   - Encryption: Uses Fernet encryption to secure logs before sending.
   - Decryption: The decryption.py script can decrypt logs when provided with the correct encryption key.

## Installation

### Prerequisites

Ensure you have the following dependencies installed:
```
pip install cryptography pynput pyaudio pillow requests
```

## Usage

### Generating an Encryption Key

Run the `key_gen.py` script to generate an encryption key:
```
python key_gen.py
```
This will create a `encryption_key.txt` file containing the encryption key.

### Running the Keylogger

Execute the keylogger script to start logging and encryption:
```
python keylogger.py
```
- The script logs keystrokes, captures system details, records audio, and takes screenshots.
- Encrypted logs are saved in `e_sys_details.txt` and `e_key_log.txt`.
- Emails the encrypted logs to the specified recipient.

### Decrypting Logs

To decrypt encrypted logs, run:
```
python decryption.py
```
This will restore the original log files using the encryption key from `encryption_key.txt`.

## Notes

Ensure `encryption_key.txt` is securely stored, as it is required for decryption.
