import os
import base64
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from cryptography.fernet import Fernet
from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/decrypt_link', methods=['GET', 'POST'])
def decrypt_link():
    decrypted = error = None
    encrypted = request.args.get('encrypted') or request.form.get('encrypted')

    if not encrypted:
        error = "No encrypted link provided."
    elif request.method == 'POST':
        key = request.form.get('key', '')
        if key and len(key) == 10 and key.isdigit():
            try:
                custom_key = key.ljust(32, '0').encode()
                cipher_suite = Fernet(base64.urlsafe_b64encode(custom_key))
                decrypted = cipher_suite.decrypt(encrypted.encode()).decode()
            except Exception as e:
                error = f"Decryption failed: {str(e)}"
        else:
            error = "Please enter a valid 10-digit numeric key."

    return render_template('decrypt_link.html', encrypted=encrypted, decrypted=decrypted, error=error)

# Local-only logic
if __name__ == "__main__" and os.environ.get("WERKZEUG_RUN_MAIN") != "true":
    settings_file_path = "client_secrets.json"

    if not os.path.exists(settings_file_path):
        raise FileNotFoundError(f"No such file or directory: '{settings_file_path}'")

    print("File found")

    gauth = GoogleAuth()
    gauth.settings_file = settings_file_path
    gauth.LoadClientConfigFile(settings_file_path)
    gauth.LocalWebserverAuth()

    drive = GoogleDrive(gauth)

    file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
    print("Files in Google Drive:")
    for i, file in enumerate(file_list):
        print(f"{i + 1}. Title: {file['title']}, ID: {file['id']}")

    file_number = int(input("Enter the number of the file you want to choose: ")) - 1
    selected_file = file_list[file_number]

    print(f"Selected file: Title: {selected_file['title']}, ID: {selected_file['id']}")

    permission = selected_file.InsertPermission({
        'type': 'anyone',
        'role': 'writer'
    })
    print(f"Permission granted to anyone for file: {selected_file['title']}")

    custom_key_input = input("Enter your custom encryption key (10 digits): ")
    if len(custom_key_input) != 10 or not custom_key_input.isdigit():
        raise ValueError("The custom encryption key must be exactly 10 digits long.")

    custom_key = custom_key_input.ljust(32, '0').encode()
    cipher_suite = Fernet(base64.urlsafe_b64encode(custom_key))
    shared_link = f'https://drive.google.com/file/d/{selected_file["id"]}/view'
    encrypted_link = cipher_suite.encrypt(shared_link.encode()).decode()

    print(f'Encrypted link: {encrypted_link}')
    print(f'Decryption key: {custom_key_input}')

    # Cloud Run URL
    cloud_run_url = "https://secure-decryptor-1068809376566.us-central1.run.app"
    decryption_page_url = f"{cloud_run_url}/decrypt_link?encrypted={encrypted_link}"
    print(f"\nSend this link to decrypt the file:\n{decryption_page_url}")

    sender_email = "trinabshan06@gmail.com"
    receiver_email = "trinabtime@gmail.com"
    password = "yhcq gspr pnal rlfu"  # App Password

    message = MIMEMultipart("alternative")
    message["Subject"] = "Encrypted Google Drive Link"
    message["From"] = sender_email
    message["To"] = receiver_email

    text = f"""
Hello Kiruba mama,

If you get an email like this from another gmail (trinabtime@gmail.com), I want you to ignore it because I sent it by mistake.
Kindly excuse me for that mama.

I have created an encrypted Google Drive link and hosted a secure decryption service on Google Cloud Platform (GCP).

To decrypt and access the file, go to the following URL and enter the decryption key:

🔓 Decryption Page:  
{decryption_page_url}

🔐 Decryption Key: {custom_key_input}

This page will allow you to enter the key and reveal the original link securely.

Thank You,
Trinab Shan
"""

    part = MIMEText(text, "plain")
    message.attach(part)

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())
            print("Email sent successfully!")
    except Exception as e:
        print(f"An error occurred while sending the email: {e}")
