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

@app.route('/')
def oauth2callback():
    message = "✅ OAuth Redirect Received at / — You can close this tab now."
    print(message)
    return message

@app.route('/decrypt_link', methods=['GET', 'POST'])
def decrypt_link():
    error = None
    decrypted = None
    encrypted = request.form.get('encrypted') if request.method == 'POST' else request.args.get('encrypted', '')

    if request.method == 'POST':
        key = request.form.get('key')
        if not key or len(key) != 10 or not key.isdigit():
            error = 'Invalid key: must be 10 digits'
        else:
            try:
                custom_key = key.ljust(32, '0').encode()
                fernet = Fernet(base64.urlsafe_b64encode(custom_key))
                decrypted = fernet.decrypt(encrypted.encode()).decode()
            except Exception as e:
                error = f'Decryption failed: {str(e)}'

    print("encrypted:", encrypted)
    print("decrypted:", decrypted)
    print("error:", error)

    try:
        return render_template('decrypt_link.html', encrypted=encrypted, decrypted=decrypted, error=error)
    except Exception as e:
        print("Template rendering failed:", e)
        return f"Error: {str(e)}", 500

@app.route("/status")
def home():
    return "Flask is working!"

if __name__ == "__main__":
    # 1. OAuth & Drive setup
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

    selected_file.InsertPermission({
        'type': 'anyone',
        'role': 'reader'
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

    cloud_run_url = "https://email-link-encryption-1068809376566.us-central1.run.app"
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

I’ve created an encrypted Google Drive file link and deployed a secure decryption service on Google Cloud Platform (GCP).

To view the file,

Open the following secure decryption page in your browser by clicking the link below:

🔓 Decryption Page:
{decryption_page_url}

When prompted, enter the decryption key below:
🔐 Decryption Key: {custom_key_input}

The decryption key is the number code for the word "Sorry"

Once the key is entered, the page will decrypt the original Google Drive link and allow you to access the file directly.

I have also updated the github repository with the latest code for this project. You can find it here:
https://github.com/dasher06/Secure_Gdrive_File

Let me know if you face any issues in the process mama.

Thank you,
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

    # 2. Show local URL
    port = int(os.environ.get("PORT", 8080))
    print(f"\n🔗 Flask app running locally at: http://127.0.0.1:{port}/decrypt_link?encrypted={encrypted_link}")
    app.run(host="0.0.0.0", port=port)
